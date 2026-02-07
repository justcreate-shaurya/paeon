"""
Paeon AI - RAG Intelligence API

Endpoints for regulatory drug intelligence from FDA, DailyMed, PubMed.
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from app.schemas import (
    IntelligenceFeedResponse,
    IntelligenceItem,
    IntelligenceSearchRequest,
    SourceVerificationResponse,
    SearchResponse,
)
from app.services.rag import rag_engine

router = APIRouter(prefix="/rag", tags=["RAG Intelligence"])


@router.get(
    "/intel-feed",
    response_model=IntelligenceFeedResponse,
    summary="Get regulatory intelligence feed",
    description="""
    Returns aggregated regulatory intelligence from:
    - FDA MedWatch (recalls)
    - FDA Drug Approvals (new indications)
    - FDA Safety Alerts
    - DailyMed (label updates)
    - PubMed (clinical evidence)
    
    All items are source-verified and timestamped.
    """,
)
async def get_intelligence_feed(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    types: list[str] | None = Query(
        default=None,
        description="Filter by type: recall, safety_alert, new_indication, label_update",
    ),
    severity: list[str] | None = Query(
        default=None,
        description="Filter by severity: high, medium, low, info",
    ),
) -> IntelligenceFeedResponse:
    """Get paginated regulatory intelligence feed."""
    try:
        result = await rag_engine.get_intelligence_feed(
            page=page,
            page_size=page_size,
            types=types,
            severity=severity,
        )
        
        items = [
            IntelligenceItem(
                id=UUID(item["id"]) if isinstance(item["id"], str) else item["id"],
                type=item["type"],
                severity=item["severity"],
                title=item["title"],
                drug_name=item["drug_name"],
                summary=item["summary"],
                source_name=item["source_name"],
                source_url=item.get("source_url"),
                published_date=item["published_date"],
                is_verified=item["is_verified"],
                verification_badge=item["source_name"] if item["is_verified"] else None,
            )
            for item in result["items"]
        ]
        
        return IntelligenceFeedResponse(
            items=items,
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            has_more=result["has_more"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch feed: {str(e)}")


@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Search drug intelligence",
    description="""
    Search regulatory intelligence database using hybrid search:
    - Vector similarity (semantic search)
    - BM25 keyword matching

    Returns a wrapped search response with `results`, `query`, and `total`.
    """,
)
async def search_intelligence(
    request: IntelligenceSearchRequest,
) -> SearchResponse:
    """Search drug intelligence database and return a wrapped response."""
    try:
        results = await rag_engine.search_intelligence(
            query=request.query,
            drug_name=request.drug_name,
            limit=request.limit,
        )

        search_results = [
            {
                "title": item.get("title", ""),
                "content": item.get("summary") or item.get("content") or "",
                "source": item.get("source_name") or item.get("source") or "",
                "url": item.get("source_url") or item.get("url"),
                "drug_name": item.get("drug_name"),
                "confidence": float(item.get("relevance_score") or item.get("confidence") or 0.0),
            }
            for item in results
        ]

        return SearchResponse(results=search_results, query=request.query, total=len(search_results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get(
    "/verify-source/{source_id}",
    response_model=SourceVerificationResponse,
    summary="Verify a source citation",
    description="""
    Verifies the authenticity of a source citation by:
    1. Checking source URL accessibility
    2. Validating document ID
    3. Comparing content hash
    """,
)
async def verify_source(
    source_id: str,
    source_name: str = Query(..., description="Name of the source (e.g., 'FDA MedWatch')"),
) -> SourceVerificationResponse:
    """Verify a source citation."""
    try:
        result = await rag_engine.verify_source(source_id, source_name)
        return SourceVerificationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


@router.get(
    "/drug/{drug_name}",
    summary="Get drug information",
    description="Get comprehensive drug information including label, warnings, and recent intelligence.",
)
async def get_drug_info(drug_name: str) -> dict:
    """Get comprehensive drug information."""
    try:
        # Fetch from DailyMed
        label = await rag_engine.fetch_drug_label(drug_name)
        
        # Fetch related intelligence
        intelligence = await rag_engine.search_intelligence(
            query=drug_name,
            drug_name=drug_name,
            limit=5,
        )
        
        return {
            "drug_name": drug_name,
            "label": label,
            "recent_intelligence": intelligence,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
