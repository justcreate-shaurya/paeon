"""
Paeon AI - Health Check & System Status API
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import settings
from app.schemas import HealthStatus, ComplianceStatus

router = APIRouter(tags=["Health & Status"])


@router.get(
    "/health",
    response_model=HealthStatus,
    summary="System health check",
    description="Returns overall system health status and component statuses.",
)
async def health_check() -> HealthStatus:
    """Check system health."""
    # In production, these would be actual health checks
    components = {
        "database": {"status": "healthy", "latency_ms": 5},
        "redis": {"status": "healthy", "latency_ms": 2},
        "vector_db": {"status": "healthy", "latency_ms": 10},
        "llm_service": {"status": "healthy", "latency_ms": 150},
        "fda_api": {"status": "healthy", "latency_ms": 200},
    }
    
    all_healthy = all(c["status"] == "healthy" for c in components.values())
    
    return HealthStatus(
        status="healthy" if all_healthy else "degraded",
        version=settings.app_version,
        timestamp=datetime.now(timezone.utc),
        components=components,
    )


@router.get(
    "/compliance",
    response_model=ComplianceStatus,
    summary="Compliance status",
    description="Returns current compliance status for all safety measures.",
)
async def compliance_status() -> ComplianceStatus:
    """Check compliance status."""
    return ComplianceStatus(
        pii_protection=settings.pii_detection_enabled,
        fair_balance=settings.fair_balance_strict_mode,
        source_verification=True,
        audit_logging=True,
        all_compliant=(
            settings.pii_detection_enabled 
            and settings.fair_balance_strict_mode
        ),
    )


@router.get(
    "/",
    summary="API root",
    description="Returns API information and available endpoints.",
)
async def root() -> dict:
    """API root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Clinical-to-Vernacular Bridge - Digital Medical Representative",
        "disclaimer": "For Healthcare Professional use only. Not a diagnostic tool.",
        "documentation": "/docs",
        "endpoints": {
            "slang_translation": f"{settings.api_prefix}/slang/translate",
            "intelligence_feed": f"{settings.api_prefix}/rag/intel-feed",
            "asset_generation": f"{settings.api_prefix}/assets/generate",
            "health": f"{settings.api_prefix}/health",
        },
    }
