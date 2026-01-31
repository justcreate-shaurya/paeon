"""
Paeon AI - Slang-to-Clinical Translation API

Endpoints for translating patient language to clinical terminology.
"""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.schemas import (
    TranslationRequest,
    TranslationResponse,
    TranslationFeedbackRequest,
    SupportedLanguage,
    StandardCode,
)
from app.services.slang import slang_to_clinical_engine

router = APIRouter(prefix="/slang", tags=["Slang-to-Clinical Translation"])


@router.post(
    "/translate",
    response_model=TranslationResponse,
    summary="Translate patient language to clinical terms",
    description="""
    Translates colloquial patient language from any supported language
    into structured clinical terminology with SNOMED-CT and ICD-10 codes.
    
    **IMPORTANT**: This is NOT a diagnostic tool. It only maps linguistic
    meaning to standardized medical vocabulary.
    
    The system:
    - Detects input language automatically
    - Strips any PII before processing
    - Maps to SNOMED-CT and ICD-10 codes
    - Provides confidence scores
    - Validates output for medical safety
    """,
)
async def translate_to_clinical(
    request: TranslationRequest,
    http_request: Request,
) -> TranslationResponse:
    """
    Translate patient language to clinical terminology.
    
    Examples:
    - "my heart feels funny" → Palpitations (SNOMED: 80313002)
    - "mere seene mein dard" (Hindi) → Chest Pain (SNOMED: 29857009)
    """
    try:
        result = await slang_to_clinical_engine.translate(
            text=request.text,
            context=request.context,
            session_id=request.session_id,
        )
        
        return TranslationResponse(
            id=UUID(result["id"]),
            original_language=result["original_language"],
            raw_input=result["raw_input"],
            normalized_english=result["normalized_english"],
            clinical_interpretation=result["clinical_interpretation"],
            standard_codes=[
                StandardCode(**code) for code in result["standard_codes"]
            ],
            confidence=result["confidence"],
            rationale=result["rationale"],
            processing_time_ms=result["processing_time_ms"],
            created_at=datetime.now(timezone.utc),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.get(
    "/languages",
    response_model=list[SupportedLanguage],
    summary="Get supported input languages",
    description="Returns list of all supported languages for patient input.",
)
async def get_supported_languages() -> list[SupportedLanguage]:
    """Get list of supported input languages."""
    languages = slang_to_clinical_engine.get_supported_languages()
    return [SupportedLanguage(**lang) for lang in languages]


@router.post(
    "/translations/{translation_id}/feedback",
    summary="Submit clinician feedback on translation",
    description="""
    Allows clinicians to approve or correct a translation.
    This feedback is used to improve the system over time.
    """,
)
async def submit_feedback(
    translation_id: UUID,
    feedback: TranslationFeedbackRequest,
) -> dict:
    """Submit clinician feedback on a translation."""
    # In production, this would update the database
    return {
        "status": "success",
        "message": "Feedback recorded",
        "translation_id": str(translation_id),
        "approved": feedback.approved,
    }


class QuickTranslateRequest(BaseModel):
    """Quick translation request for demo purposes."""
    text: str


@router.post(
    "/quick-translate",
    summary="Quick translation for demo",
    description="Simplified translation endpoint for demos and testing.",
)
async def quick_translate(request: QuickTranslateRequest) -> dict:
    """Quick translation without full validation."""
    try:
        result = await slang_to_clinical_engine.translate(
            text=request.text,
            context=None,
            session_id=None,
        )
        
        return {
            "input": result["raw_input"],
            "language": result["original_language"],
            "clinical": result["clinical_interpretation"],
            "confidence": int(result["confidence"] * 100),
            "codes": result["standard_codes"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
