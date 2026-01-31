"""
Paeon AI - Asset Generation API

Endpoints for generating Fair Balance compliant patient education materials.
"""

from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.schemas import (
    AssetGenerationRequest,
    GeneratedAsset,
    AssetExportRequest,
    AssetExportResponse,
)
from app.services.assets import fair_balance_engine

router = APIRouter(prefix="/assets", tags=["Asset Generation"])

# In-memory cache for generated assets (use Redis in production)
_asset_cache: dict[str, dict] = {}


@router.post(
    "/generate",
    response_model=GeneratedAsset,
    summary="Generate patient education asset",
    description="""
    Generates a Fair Balance compliant patient education card for a drug.
    
    The asset includes:
    - Drug name and dosage
    - How to take instructions
    - Key benefits (balanced with risks)
    - Safety information
    - Contraindications
    - Black box warning (if applicable)
    - Required disclaimers
    
    All assets are validated for Fair Balance compliance before return.
    """,
)
async def generate_asset(request: AssetGenerationRequest) -> GeneratedAsset:
    """Generate a patient education asset."""
    try:
        card = await fair_balance_engine.generate_patient_card(
            drug_name=request.drug_name,
            dosage=request.dosage,
            indication=request.indication,
            include_black_box=request.include_black_box,
        )
        
        # Cache the asset
        _asset_cache[card["id"]] = card
        
        return GeneratedAsset(
            id=UUID(card["id"]),
            drug_name=card["drug_name"],
            dosage=card.get("dosage"),
            title=card["title"],
            how_to_take=card["how_to_take"],
            key_benefits=card["key_benefits"],
            safety_information=card["safety_information"],
            contraindications=card["contraindications"],
            black_box_warning=card.get("black_box_warning"),
            disclaimer=card["disclaimer"],
            fair_balance_score=card["fair_balance_score"],
            compliance_verified=card["compliance_verified"],
            created_at=card["created_at"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Asset generation failed: {str(e)}")


@router.get(
    "/{asset_id}",
    response_model=GeneratedAsset,
    summary="Get a generated asset",
)
async def get_asset(asset_id: UUID) -> GeneratedAsset:
    """Retrieve a previously generated asset."""
    card = _asset_cache.get(str(asset_id))
    if not card:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return GeneratedAsset(
        id=UUID(card["id"]),
        drug_name=card["drug_name"],
        dosage=card.get("dosage"),
        title=card["title"],
        how_to_take=card["how_to_take"],
        key_benefits=card["key_benefits"],
        safety_information=card["safety_information"],
        contraindications=card["contraindications"],
        black_box_warning=card.get("black_box_warning"),
        disclaimer=card["disclaimer"],
        fair_balance_score=card["fair_balance_score"],
        compliance_verified=card["compliance_verified"],
        created_at=card["created_at"],
    )


@router.post(
    "/export/pdf",
    summary="Export asset as PDF",
    description="Export a patient education asset as a PDF document.",
)
async def export_pdf(request: AssetExportRequest) -> Response:
    """Export asset as PDF."""
    card = _asset_cache.get(str(request.asset_id))
    if not card:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    try:
        pdf_bytes = await fair_balance_engine.export_to_pdf(card)
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=patient_card_{card['drug_name']}.pdf"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")


@router.post(
    "/export/png",
    summary="Export asset as PNG",
    description="Export a patient education asset as a PNG image.",
)
async def export_png(request: AssetExportRequest) -> Response:
    """Export asset as PNG."""
    card = _asset_cache.get(str(request.asset_id))
    if not card:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    try:
        png_bytes = await fair_balance_engine.export_to_png(card)
        
        return Response(
            content=png_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename=patient_card_{card['drug_name']}.png"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PNG export failed: {str(e)}")


@router.post(
    "/quick-generate",
    summary="Quick asset generation for demo",
    description="Simplified endpoint for generating assets in demos.",
)
async def quick_generate(drug_name: str, dosage: str = None) -> dict:
    """Quick asset generation for demos."""
    try:
        card = await fair_balance_engine.generate_patient_card(
            drug_name=drug_name,
            dosage=dosage,
        )
        
        _asset_cache[card["id"]] = card
        
        return {
            "id": card["id"],
            "drug_name": card["drug_name"],
            "dosage": card.get("dosage"),
            "how_to_take": card["how_to_take"],
            "benefits": card["key_benefits"],
            "safety": card["safety_information"],
            "black_box": card.get("black_box_warning"),
            "disclaimer": card["disclaimer"],
            "fair_balance_score": card["fair_balance_score"],
            "compliance_verified": card["compliance_verified"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/drugs/available",
    summary="Get list of drugs with detailed information",
    description="Returns list of drugs that have detailed information available.",
)
async def get_available_drugs() -> list[dict]:
    """Get list of drugs with detailed information."""
    drugs = list(fair_balance_engine.DRUG_DATABASE.keys())
    return [
        {
            "name": drug.title(),
            "brand_names": fair_balance_engine.DRUG_DATABASE[drug].get("brand_names", []),
            "drug_class": fair_balance_engine.DRUG_DATABASE[drug].get("drug_class", ""),
        }
        for drug in drugs
    ]
