"""
Paeon AI - Slang-to-Clinical Translation Engine

This is the core linguistic mapping system that transforms
colloquial patient language into structured clinical terminology.

CRITICAL SAFETY RULES:
- This engine does NOT diagnose
- This engine does NOT prescribe
- This engine ONLY performs linguistic semantic normalization
"""

import hashlib
import json
import logging
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Any
from uuid import uuid4

from langdetect import detect, LangDetectException

from app.core.config import settings
from app.services.compliance.pii_stripper import PIIStripper
from app.services.compliance.safety_validator import SafetyValidator

logger = logging.getLogger(__name__)

# Thread pool for LLM calls to prevent blocking the async event loop
_llm_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="llm_")


class SlangToClinicalEngine:
    """
    Multi-language clinical semantic normalization engine.
    
    Pipeline:
    1. PII Detection & Stripping
    2. Language Detection
    3. Linguistic Adaptation (LLM)
    4. Semantic Normalization
    5. Clinical Mapping (SNOMED/UMLS)
    6. Confidence Scoring
    7. Safety Validation
    """

    # Supported languages with ISO 639-1 codes
    SUPPORTED_LANGUAGES = {
        "en": ("English", "English"),
        "hi": ("Hindi", "हिन्दी"),
        "es": ("Spanish", "Español"),
        "fr": ("French", "Français"),
        "de": ("German", "Deutsch"),
        "pt": ("Portuguese", "Português"),
        "zh-cn": ("Chinese (Simplified)", "简体中文"),
        "ja": ("Japanese", "日本語"),
        "ko": ("Korean", "한국어"),
        "ar": ("Arabic", "العربية"),
        "ru": ("Russian", "Русский"),
        "ta": ("Tamil", "தமிழ்"),
        "te": ("Telugu", "తెలుగు"),
        "bn": ("Bengali", "বাংলা"),
        "mr": ("Marathi", "मराठी"),
        "gu": ("Gujarati", "ગુજરાતી"),
        "kn": ("Kannada", "ಕನ್ನಡ"),
        "ml": ("Malayalam", "മലയാളം"),
        "pa": ("Punjabi", "ਪੰਜਾਬੀ"),
        "ur": ("Urdu", "اردو"),
    }

    # Common colloquial to clinical mappings (curated knowledge base)
    CURATED_MAPPINGS = {
        # Cardiac
        "heart feels funny": {
            "clinical": "Palpitations",
            "snomed": "80313002",
            "icd10": "R00.2",
            "body_system": "cardiovascular"
        },
        "chest is tight": {
            "clinical": "Chest Tightness",
            "snomed": "23924001",
            "icd10": "R07.89",
            "body_system": "cardiovascular"
        },
        "chest pain": {
            "clinical": "Chest Tightness",
            "snomed": "23924001",
            "icd10": "R07.89",
            "body_system": "cardiovascular"
        },
        "chest tightness": {
            "clinical": "Chest Tightness",
            "snomed": "23924001",
            "icd10": "R07.89",
            "body_system": "cardiovascular"
        },
        "heart racing": {
            "clinical": "Tachycardia",
            "snomed": "3424008",
            "icd10": "R00.0",
            "body_system": "cardiovascular"
        },
        "heart skipping": {
            "clinical": "Cardiac Arrhythmia",
            "snomed": "698247007",
            "icd10": "I49.9",
            "body_system": "cardiovascular"
        },
        
        # Respiratory
        "cold": {
            "clinical": "Cold/Upper Respiratory Infection",
            "snomed": "82272006",
            "icd10": "J06.9",
            "body_system": "respiratory"
        },
        "can't breathe": {
            "clinical": "Dyspnea",
            "snomed": "267036007",
            "icd10": "R06.00",
            "body_system": "respiratory"
        },
        "short of breath": {
            "clinical": "Dyspnea",
            "snomed": "267036007",
            "icd10": "R06.00",
            "body_system": "respiratory"
        },
        "wheezing": {
            "clinical": "Wheezing",
            "snomed": "56018004",
            "icd10": "R06.2",
            "body_system": "respiratory"
        },
        
        # Gastrointestinal
        "stomach is churning": {
            "clinical": "Nausea",
            "snomed": "422587007",
            "icd10": "R11.0",
            "body_system": "gastrointestinal"
        },
        "feeling bloated": {
            "clinical": "Bloating",
            "snomed": "248490000",
            "icd10": "R14.0",
            "body_system": "gastrointestinal"
        },
        "bloated": {
            "clinical": "Bloating",
            "snomed": "248490000",
            "icd10": "R14.0",
            "body_system": "gastrointestinal"
        },
        "throwing up": {
            "clinical": "Vomiting",
            "snomed": "422400008",
            "icd10": "R11.10",
            "body_system": "gastrointestinal"
        },
        "belly hurts": {
            "clinical": "Abdominal Pain",
            "snomed": "21522001",
            "icd10": "R10.9",
            "body_system": "gastrointestinal"
        },
        "runs": {
            "clinical": "Diarrhea",
            "snomed": "62315008",
            "icd10": "R19.7",
            "body_system": "gastrointestinal"
        },
        
        # Neurological
        "head is pounding": {
            "clinical": "Headache",
            "snomed": "25064002",
            "icd10": "R51.9",
            "body_system": "neurological"
        },
        "dizzy": {
            "clinical": "Dizziness",
            "snomed": "404640003",
            "icd10": "R42",
            "body_system": "neurological"
        },
        "seeing double": {
            "clinical": "Diplopia",
            "snomed": "24982008",
            "icd10": "H53.2",
            "body_system": "neurological"
        },
        "numb": {
            "clinical": "Paresthesia",
            "snomed": "91019004",
            "icd10": "R20.2",
            "body_system": "neurological"
        },
        "burning feet": {
            "clinical": "Burning Feet Sensation",
            "snomed": "39072002",
            "icd10": "R20.8",
            "body_system": "neurological"
        },
        "feet burning": {
            "clinical": "Burning Feet Sensation",
            "snomed": "39072002",
            "icd10": "R20.8",
            "body_system": "neurological"
        },
        "burning": {
            "clinical": "Burning Sensation",
            "snomed": "19387006",
            "icd10": "R20.8",
            "body_system": "skin"
        },
        
        # Musculoskeletal
        "joints are stiff": {
            "clinical": "Joint Stiffness",
            "snomed": "84445001",
            "icd10": "M25.60",
            "body_system": "musculoskeletal"
        },
        "back is killing me": {
            "clinical": "Severe Back Pain",
            "snomed": "161891005",
            "icd10": "M54.9",
            "body_system": "musculoskeletal"
        },
        "back pain": {
            "clinical": "Back Pain",
            "snomed": "161891005",
            "icd10": "M54.9",
            "body_system": "musculoskeletal"
        },
        "muscles ache": {
            "clinical": "Myalgia",
            "snomed": "68962001",
            "icd10": "M79.1",
            "body_system": "musculoskeletal"
        },
        "muscle pain": {
            "clinical": "Myalgia",
            "snomed": "68962001",
            "icd10": "M79.1",
            "body_system": "musculoskeletal"
        },
        "my legs hurt": {
            "clinical": "Leg Pain",
            "snomed": "10601006",
            "icd10": "M79.3",
            "body_system": "musculoskeletal"
        },
        "leg pain": {
            "clinical": "Leg Pain",
            "snomed": "10601006",
            "icd10": "M79.3",
            "body_system": "musculoskeletal"
        },
        "legs hurt": {
            "clinical": "Leg Pain",
            "snomed": "10601006",
            "icd10": "M79.3",
            "body_system": "musculoskeletal"
        },
        "arm pain": {
            "clinical": "Arm Pain",
            "snomed": "3877011000036101",
            "icd10": "M79.8",
            "body_system": "musculoskeletal"
        },
        "my arms hurt": {
            "clinical": "Arm Pain",
            "snomed": "3877011000036101",
            "icd10": "M79.8",
            "body_system": "musculoskeletal"
        },
        "neck pain": {
            "clinical": "Cervical Pain",
            "snomed": "81680005",
            "icd10": "M54.2",
            "body_system": "musculoskeletal"
        },
        
        # General/Systemic
        "feeling tired": {
            "clinical": "Fatigue",
            "snomed": "84229001",
            "icd10": "R53.83",
            "body_system": "general"
        },
        "no energy": {
            "clinical": "Fatigue",
            "snomed": "84229001",
            "icd10": "R53.83",
            "body_system": "general"
        },
        "fever": {
            "clinical": "Pyrexia",
            "snomed": "386661006",
            "icd10": "R50.9",
            "body_system": "general"
        },
        "chills": {
            "clinical": "Chills",
            "snomed": "43724002",
            "icd10": "R68.83",
            "body_system": "general"
        },
        "sweating": {
            "clinical": "Hyperhidrosis",
            "snomed": "52613005",
            "icd10": "R61",
            "body_system": "general"
        },
    }

    def __init__(self):
        """Initialize the engine with required components."""
        self.pii_stripper = PIIStripper()
        self.safety_validator = SafetyValidator()
        self._llm_client = None

    @property
    def llm_client(self):
        """Lazy initialization of LLM client."""
        if self._llm_client is None:
            import google.generativeai as genai
            genai.configure(api_key=settings.gemini_api_key)
            self._llm_client = genai.GenerativeModel(settings.gemini_model)
        return self._llm_client

    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text.
        
        Returns ISO 639-1 language code.
        """
        try:
            detected = detect(text)
            # Normalize some language codes
            if detected == "zh-cn" or detected == "zh-tw":
                return "zh-cn"
            return detected if detected in self.SUPPORTED_LANGUAGES else "en"
        except LangDetectException:
            return "en"  # Default to English

    def get_language_name(self, code: str) -> str:
        """Get human-readable language name from code."""
        if code in self.SUPPORTED_LANGUAGES:
            return self.SUPPORTED_LANGUAGES[code][0]
        return "Unknown"

    def normalize_to_english(self, text: str, source_language: str) -> str:
        """
        Normalize input text to English canonical form.
        
        This uses an LLM as a LINGUISTIC ADAPTER ONLY.
        The LLM must NOT:
        - Diagnose
        - Suggest treatments
        - Mention specific drugs
        - Infer diseases
        
        It ONLY transforms linguistic meaning.
        """
        if source_language == "en":
            return self._normalize_english_text(text)

        prompt = f"""You are a clinical linguistic adapter. Your ONLY job is to translate 
patient descriptions from {self.get_language_name(source_language)} to English.

CRITICAL RULES:
1. You are NOT a doctor - do NOT diagnose
2. You are NOT a pharmacist - do NOT mention drugs
3. You are NOT providing medical advice
4. You ONLY translate the linguistic meaning

Translate this patient description to plain English, preserving the exact meaning
without adding any medical interpretation:

Input ({self.get_language_name(source_language)}): {text}

Output (English translation only, no medical terms):"""

        try:
            response = self.llm_client.generate_content(
                contents=prompt,
                generation_config={
                    "max_output_tokens": 200,
                    "temperature": 0.1,
                }
            )
            return response.text.strip()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"LLM normalization failed: {str(e)}. Using original text.")
            return text

    def _normalize_english_text(self, text: str) -> str:
        """Normalize English text to canonical form."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove filler words
        fillers = ["um", "uh", "like", "you know", "basically", "literally"]
        for filler in fillers:
            text = re.sub(rf"\b{filler}\b", "", text)
        
        # Normalize whitespace
        text = " ".join(text.split())
        
        return text

    def find_curated_mapping(self, normalized_text: str) -> dict[str, Any] | None:
        """
        Search curated mappings for known expressions.
        
        Returns mapping if confidence threshold met.
        """
        normalized_lower = normalized_text.lower()
        
        best_match = None
        best_score = 0.0
        
        for expression, mapping in self.CURATED_MAPPINGS.items():
            # Check for exact substring match
            if expression in normalized_lower:
                score = len(expression) / len(normalized_lower)
                if score > best_score:
                    best_score = score
                    best_match = {**mapping, "matched_expression": expression}
            
            # Check for word overlap
            expr_words = set(expression.split())
            text_words = set(normalized_lower.split())
            overlap = len(expr_words & text_words) / len(expr_words)
            
            if overlap > 0.7 and overlap > best_score:
                best_score = overlap
                best_match = {**mapping, "matched_expression": expression}
        
        if best_match and best_score > 0.5:
            best_match["match_score"] = best_score
            return best_match
        
        return None

    async def map_to_clinical_terms(self, normalized_text: str) -> dict[str, Any]:
        """
        Map normalized text to clinical terminology using:
        1. Curated mappings (highest priority)
        2. LLM semantic mapping for unknown symptoms
        """
        import asyncio
        
        # Try curated mappings first
        curated = self.find_curated_mapping(normalized_text)
        if curated:
            return {
                "clinical_interpretation": curated["clinical"],
                "standard_codes": [
                    {
                        "system": "SNOMED-CT",
                        "code": curated["snomed"],
                        "display": curated["clinical"]
                    },
                    {
                        "system": "ICD-10",
                        "code": curated["icd10"],
                        "display": curated["clinical"]
                    }
                ],
                "confidence": min(0.95, 0.7 + curated["match_score"] * 0.25),
                "rationale": f"Matched curated mapping for '{curated['matched_expression']}'. "
                           f"Body system: {curated['body_system']}.",
                "source": "curated_mapping"
            }

        # Use LLM for unknown symptoms - run in thread pool to avoid blocking
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, self._llm_clinical_mapping, normalized_text)
            return result
        except Exception as e:
            logger.error(f"LLM failed for '{normalized_text}': {type(e).__name__}: {str(e)}", exc_info=True)
            # Fallback if LLM fails - return Unspecified with confidence 0.5
            return {
                "clinical_interpretation": "Unspecified",
                "standard_codes": [
                    {"system": "SNOMED-CT", "code": "267038008", "display": "Unspecified"},
                    {"system": "ICD-10", "code": "R68.89", "display": "Unspecified"}
                ],
                "confidence": 0.5,
                "rationale": f"Unable to interpret symptom. LLM error: {type(e).__name__}",
                "source": "fallback"
            }

    # LLM term to codes mapping - for terms returned by LLM
    LLM_TERM_CODES = {
        "tinnitus": ("Tinnitus", "60862009", "H93.1"),
        "ear ringing": ("Tinnitus", "60862009", "H93.1"),
        "ringing ears": ("Tinnitus", "60862009", "H93.1"),
        "ringing in ears": ("Tinnitus", "60862009", "H93.1"),
        "jaw pain": ("Jaw Pain", "30968004", "K08.8"),
        "mandibular pain": ("Jaw Pain", "30968004", "K08.8"),
        "temporomandibular": ("TMJ Disorder", "91619002", "K07.6"),
        "tmj": ("TMJ Disorder", "91619002", "K07.6"),
        "swollen glands": ("Lymphadenopathy", "30746007", "R59.9"),
        "lymph nodes": ("Lymphadenopathy", "30746007", "R59.9"),
        "sore throat": ("Pharyngitis", "405737000", "J00"),
        "throat pain": ("Pharyngitis", "405737000", "J00"),
        "difficulty swallowing": ("Dysphagia", "40739000", "R13.1"),
        "difficulty breathing": ("Dyspnea", "267036007", "R06.0"),
        "back stiffness": ("Spinal Stiffness", "249917008", "M54.5"),
        "stiff neck": ("Neck Stiffness", "249917008", "M54.2"),
        "tremor": ("Tremor", "26079004", "R25.1"),
        "shaking": ("Tremor", "26079004", "R25.1"),
        "muscle weakness": ("Muscle Weakness", "26544005", "M62.8"),
        "weakness": ("Generalized Weakness", "80449002", "R53.1"),
        "headache": ("Headache", "25064002", "R51.9"),
        "head pain": ("Headache", "25064002", "R51.9"),
        "splitting headache": ("Severe Headache", "25064002", "R51.9"),
        "migraine": ("Migraine", "37796009", "G43.9"),
        "vision problems": ("Visual Disturbance", "63033001", "H53.9"),
        "blurred vision": ("Blurred Vision", "4148004", "H53.8"),
        "eye pain": ("Ocular Pain", "40638003", "H57.1"),
        "ear pain": ("Otalgia", "16001004", "H92.0"),
        "ear ache": ("Otalgia", "16001004", "H92.0"),
        "shoulder pain": ("Shoulder Pain", "55680006", "M25.51"),
        "hip pain": ("Hip Pain", "30989003", "M25.55"),
        "knee pain": ("Knee Pain", "30989003", "M25.56"),
        "ankle pain": ("Ankle Pain", "10601006", "M25.57"),
        "foot pain": ("Foot Pain", "47411000", "M79.3"),
        "skin rash": ("Rash", "271807003", "R21"),
        "rash": ("Rash", "271807003", "R21"),
        "itching": ("Pruritus", "418290006", "L29.9"),
        "itchy": ("Pruritus", "418290006", "L29.9"),
        "hives": ("Urticaria", "126485001", "L50.9"),
        "skin irritation": ("Dermatitis", "24075002", "L30.9"),
        "dry skin": ("Xerosis", "16386004", "L85.3"),
        "skin sores": ("Skin Lesion", "95320000", "L98.9"),
        "mouth ulcer": ("Oral Ulcer", "2092003", "K12.1"),
        "canker sore": ("Oral Ulcer", "2092003", "K12.1"),
        "lip swelling": ("Lip Edema", "423666004", "R60.0"),
        "tongue swelling": ("Glossitis", "76529007", "K14.0"),
        "bad taste": ("Dysgeusia", "367069002", "R43.2"),
        "metallic taste": ("Dysgeusia", "367069002", "R43.2"),
    }

    def _llm_clinical_mapping(self, normalized_text: str) -> dict[str, Any]:
        """
        Use LLM to map text to clinical terminology.
        Ask for plain text response, not JSON.
        """
        try:
            # Ask for just the clinical term in plain English
            prompt = f'What medical/clinical term describes this patient symptom in just 1-3 words: "{normalized_text}"? Answer with ONLY the clinical term, nothing else.'
            
            # Call Gemini with high tokens and low temperature
            response = self.llm_client.generate_content(
                contents=prompt,
                generation_config={
                    "max_output_tokens": 500,  # Much higher
                    "temperature": 0.3,  # Slightly creative
                }
            )
            
            response_text = (response.text if hasattr(response, 'text') else "").strip()
            logger.info(f"[LLM] Plain text response: {repr(response_text)}")
            
            if not response_text or len(response_text) < 2:
                raise ValueError(f"LLM returned empty or too short: {repr(response_text)}")
            
            # Clean up response - remove quotes, asterisks, etc
            response_text = response_text.strip('"\'*- ').lower()
            
            # Try to find matching codes
            clinical_term = None
            snomed_code = "267038008"  # Default: Unspecified
            icd10_code = "R68.89"      # Default: Unspecified
            
            # First try exact match in our mapping
            if response_text in self.LLM_TERM_CODES:
                clinical_term, snomed_code, icd10_code = self.LLM_TERM_CODES[response_text]
            else:
                # Try partial matching
                response_lower = response_text.lower()
                for term, (clinical, snomed, icd10) in self.LLM_TERM_CODES.items():
                    if term in response_lower or response_lower in term:
                        clinical_term = clinical
                        snomed_code = snomed
                        icd10_code = icd10
                        break
            
            # If no match found, use the LLM response as the clinical term itself
            if not clinical_term:
                clinical_term = response_text.title()
            
            logger.info(f"[LLM] Mapped to: {clinical_term} ({snomed_code}/{icd10_code})")
            
            return {
                "clinical_interpretation": clinical_term,
                "standard_codes": [
                    {"system": "SNOMED-CT", "code": snomed_code, "display": clinical_term},
                    {"system": "ICD-10", "code": icd10_code, "display": clinical_term}
                ],
                "confidence": 0.75,
                "rationale": f"AI interpreted '{normalized_text}' as {clinical_term}",
                "source": "llm_mapping"
            }
            
        except Exception as e:
            logger.error(f"[LLM] Failed: {type(e).__name__}: {e}")
            raise

    async def translate(
        self,
        text: str,
        context: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Main translation pipeline.
        
        Transforms patient language to clinical terminology.
        """
        start_time = time.time()
        
        # Step 1: Strip PII
        stripped_text, pii_report = self.pii_stripper.strip_pii(text)
        
        # Step 2: Detect language
        detected_language = self.detect_language(stripped_text)
        
        # Step 3: Normalize to English
        normalized_english = self.normalize_to_english(stripped_text, detected_language)
        
        # Step 4: Map to clinical terms
        mapping_result = await self.map_to_clinical_terms(normalized_english)
        
        # Step 5: Safety validation
        safety_result = self.safety_validator.validate_output(
            mapping_result["clinical_interpretation"],
            mapping_result["rationale"]
        )
        
        if not safety_result["is_safe"]:
            # If output contains diagnostic/prescriptive language, sanitize
            mapping_result["clinical_interpretation"] = safety_result["sanitized_output"]
            mapping_result["rationale"] += f" [Safety note: {safety_result['reason']}]"
            mapping_result["confidence"] *= 0.7  # Reduce confidence
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "id": str(uuid4()),
            "original_language": self.get_language_name(detected_language),
            "raw_input": stripped_text,
            "normalized_english": normalized_english,
            "clinical_interpretation": mapping_result["clinical_interpretation"],
            "standard_codes": mapping_result["standard_codes"],
            "confidence": mapping_result["confidence"],
            "rationale": mapping_result["rationale"],
            "processing_time_ms": processing_time_ms,
            "pii_detected": pii_report["pii_detected"],
            "session_id": session_id,
        }

    def get_supported_languages(self) -> list[dict[str, str]]:
        """Return list of supported input languages."""
        return [
            {"code": code, "name": names[0], "native_name": names[1]}
            for code, names in self.SUPPORTED_LANGUAGES.items()
        ]


# Singleton instance
slang_to_clinical_engine = SlangToClinicalEngine()
