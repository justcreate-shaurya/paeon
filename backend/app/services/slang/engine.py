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
import re
import time
from typing import Any
from uuid import uuid4

from langdetect import detect, LangDetectException

from app.core.config import settings
from app.services.compliance.pii_stripper import PIIStripper
from app.services.compliance.safety_validator import SafetyValidator


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
        "muscles ache": {
            "clinical": "Myalgia",
            "snomed": "68962001",
            "icd10": "M79.1",
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
            from openai import OpenAI
            self._llm_client = OpenAI(api_key=settings.openai_api_key)
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
            response = self.llm_client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical linguistic translator. Translate patient descriptions to English without adding medical interpretation."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.1,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            # Fallback: return original text
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

    def map_to_clinical_terms(self, normalized_text: str) -> dict[str, Any]:
        """
        Map normalized text to clinical terminology using:
        1. Curated mappings (highest priority)
        2. LLM semantic mapping (with safety constraints)
        """
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

        # Use LLM for semantic mapping
        return self._llm_clinical_mapping(normalized_text)

    def _llm_clinical_mapping(self, normalized_text: str) -> dict[str, Any]:
        """
        Use LLM to map text to clinical terminology.
        
        The LLM acts as a semantic mapper, NOT a diagnostic tool.
        """
        prompt = f"""You are a clinical terminology mapper for a healthcare IT system.
Your job is to map patient symptom descriptions to standardized clinical terms.

CRITICAL CONSTRAINTS:
1. You are NOT diagnosing - only mapping symptoms to terminology
2. Map to symptom terms ONLY, not disease diagnoses
3. Provide SNOMED-CT and ICD-10 codes for SYMPTOMS only
4. If uncertain, indicate lower confidence

Patient description: "{normalized_text}"

Respond in this exact JSON format:
{{
    "clinical_term": "The standardized symptom term",
    "snomed_code": "SNOMED-CT code for the symptom",
    "icd10_code": "ICD-10 code for the symptom",
    "confidence": 0.0 to 1.0,
    "rationale": "Brief explanation of the mapping"
}}

If you cannot map to clinical terms with confidence, respond with:
{{
    "clinical_term": "Unspecified symptom",
    "snomed_code": "267038008",
    "icd10_code": "R68.89",
    "confidence": 0.3,
    "rationale": "Unable to map with high confidence"
}}"""

        try:
            response = self.llm_client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a clinical terminology mapping system. Output valid JSON only."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                "clinical_interpretation": result.get("clinical_term", "Unspecified symptom"),
                "standard_codes": [
                    {
                        "system": "SNOMED-CT",
                        "code": result.get("snomed_code", "267038008"),
                        "display": result.get("clinical_term", "Unspecified")
                    },
                    {
                        "system": "ICD-10",
                        "code": result.get("icd10_code", "R68.89"),
                        "display": result.get("clinical_term", "Unspecified")
                    }
                ],
                "confidence": min(0.9, result.get("confidence", 0.5)),  # Cap at 0.9 for LLM
                "rationale": result.get("rationale", "Mapped using semantic analysis"),
                "source": "llm_mapping"
            }

        except Exception as e:
            # Fallback response
            return {
                "clinical_interpretation": "Unable to interpret",
                "standard_codes": [],
                "confidence": 0.0,
                "rationale": f"Mapping failed: {str(e)}",
                "source": "error"
            }

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
        mapping_result = self.map_to_clinical_terms(normalized_english)
        
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
