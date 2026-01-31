"""
Paeon AI Backend - Pydantic Schemas

Request/Response models for API contracts.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# SLANG-TO-CLINICAL SCHEMAS
# ============================================================================

class StandardCode(BaseModel):
    """Medical standard code reference."""
    
    system: str = Field(..., description="Code system (SNOMED-CT, ICD-10, UMLS)")
    code: str = Field(..., description="The actual code")
    display: Optional[str] = Field(None, description="Human-readable display name")


class TranslationRequest(BaseModel):
    """Request to translate patient language to clinical terms."""
    
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=2000,
        description="Patient's description in any language"
    )
    context: Optional[str] = Field(
        None, 
        max_length=500,
        description="Optional clinical context"
    )
    session_id: Optional[str] = Field(None, description="Session tracking ID")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "my heart feels funny and tight",
                "context": "Patient presenting with chest discomfort",
                "session_id": "sess_abc123"
            }
        }
    )


class TranslationResponse(BaseModel):
    """Clinical translation result."""
    
    id: UUID = Field(..., description="Unique translation ID")
    original_language: str = Field(..., description="Detected source language")
    raw_input: str = Field(..., description="Original input (PII-stripped)")
    normalized_english: str = Field(..., description="English canonical form")
    clinical_interpretation: str = Field(..., description="Clinical terminology")
    standard_codes: list[StandardCode] = Field(
        default_factory=list,
        description="SNOMED/ICD/UMLS codes"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    rationale: str = Field(..., description="Explanation of the mapping")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    created_at: datetime = Field(..., description="Timestamp")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "original_language": "English",
                "raw_input": "my heart feels funny and tight",
                "normalized_english": "heart sensation abnormal with tightness",
                "clinical_interpretation": "Palpitations with Chest Tightness",
                "standard_codes": [
                    {"system": "SNOMED-CT", "code": "80313002", "display": "Palpitations"},
                    {"system": "ICD-10", "code": "R00.2", "display": "Palpitations"}
                ],
                "confidence": 0.89,
                "rationale": "Patient describes cardiac sensation abnormality...",
                "processing_time_ms": 1250,
                "created_at": "2026-01-31T10:30:00Z"
            }
        }
    )


class TranslationFeedbackRequest(BaseModel):
    """Clinician feedback on a translation."""
    
    approved: bool = Field(..., description="Whether clinician approves translation")
    correction: Optional[str] = Field(
        None, 
        max_length=1000,
        description="Corrected clinical interpretation"
    )


class SupportedLanguage(BaseModel):
    """Supported input language."""
    
    code: str = Field(..., description="ISO 639-1 language code")
    name: str = Field(..., description="Language name")
    native_name: str = Field(..., description="Native language name")


# ============================================================================
# RAG INTELLIGENCE SCHEMAS
# ============================================================================

class IntelligenceItem(BaseModel):
    """A single regulatory intelligence item."""
    
    id: UUID
    type: str = Field(..., description="recall, safety_alert, new_indication, label_update")
    severity: str = Field(..., description="high, medium, low, info")
    title: str
    drug_name: str
    summary: str
    source_name: str
    source_url: Optional[str]
    published_date: datetime
    is_verified: bool
    verification_badge: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "type": "recall",
                "severity": "high",
                "title": "FDA Drug Recall Alert",
                "drug_name": "Metformin HCl 500mg",
                "summary": "Voluntary recall due to NDMA contamination...",
                "source_name": "FDA MedWatch",
                "source_url": "https://www.fda.gov/...",
                "published_date": "2026-01-28T00:00:00Z",
                "is_verified": True,
                "verification_badge": "FDA Official"
            }
        }
    )


class IntelligenceFeedResponse(BaseModel):
    """Intelligence feed response with pagination."""
    
    items: list[IntelligenceItem]
    total: int
    page: int
    page_size: int
    has_more: bool


class IntelligenceSearchRequest(BaseModel):
    """Search request for drug intelligence."""
    
    query: str = Field(..., min_length=2, max_length=500)
    drug_name: Optional[str] = None
    types: Optional[list[str]] = Field(
        None, 
        description="Filter by intel types"
    )
    severity: Optional[list[str]] = Field(
        None,
        description="Filter by severity levels"
    )
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    limit: int = Field(default=20, ge=1, le=100)


class SearchResult(BaseModel):
    """Single search result for intelligence search."""

    title: str
    content: str
    source: str
    url: Optional[str] = None
    drug_name: Optional[str] = None
    confidence: float = Field(..., ge=0.0, le=1.0)


class SearchResponse(BaseModel):
    """Wrapped search response returned by /rag/search."""

    results: list[SearchResult]
    query: str
    total: int


class SourceVerificationResponse(BaseModel):
    """Source verification result."""
    
    source_name: str
    source_url: str
    is_verified: bool
    verification_method: str
    verification_date: datetime
    document_excerpt: str
    authority: str
    related_documents: list[dict[str, str]]


# ============================================================================
# ASSET GENERATION SCHEMAS
# ============================================================================

class AssetGenerationRequest(BaseModel):
    """Request to generate a patient education asset."""
    
    drug_name: str = Field(..., min_length=2, max_length=200)
    dosage: Optional[str] = Field(None, max_length=100)
    indication: Optional[str] = Field(None, max_length=500)
    target_audience: str = Field(default="patient", description="patient or hcp")
    language: str = Field(default="en", description="Output language")
    include_black_box: bool = Field(default=True)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "drug_name": "Metformin",
                "dosage": "500mg",
                "indication": "Type 2 Diabetes Management",
                "target_audience": "patient",
                "language": "en",
                "include_black_box": True
            }
        }
    )


class GeneratedAsset(BaseModel):
    """Generated patient education asset."""
    
    id: UUID
    drug_name: str
    dosage: Optional[str]
    title: str
    how_to_take: str
    key_benefits: list[str]
    safety_information: str
    contraindications: list[str]
    black_box_warning: Optional[str]
    disclaimer: str
    fair_balance_score: float = Field(..., ge=0.0, le=1.0)
    compliance_verified: bool
    created_at: datetime


class AssetExportRequest(BaseModel):
    """Request to export an asset."""
    
    asset_id: UUID
    format: str = Field(..., pattern="^(pdf|png)$")
    include_qr_code: bool = Field(default=False)


class AssetExportResponse(BaseModel):
    """Export result with download URL."""
    
    asset_id: UUID
    format: str
    download_url: str
    expires_at: datetime
    file_size_bytes: int


# ============================================================================
# COMPLIANCE & AUDIT SCHEMAS
# ============================================================================

class ComplianceStatus(BaseModel):
    """Overall compliance status."""
    
    pii_protection: bool
    fair_balance: bool
    source_verification: bool
    audit_logging: bool
    all_compliant: bool


class AuditLogEntry(BaseModel):
    """Single audit log entry."""
    
    id: UUID
    timestamp: datetime
    action_type: str
    resource_type: str
    resource_id: Optional[str]
    actor_id_hash: str
    confidence_score: Optional[float]
    safety_flags: list[str]


class AuditLogResponse(BaseModel):
    """Paginated audit logs."""
    
    entries: list[AuditLogEntry]
    total: int
    page: int
    page_size: int


# ============================================================================
# HEALTH & STATUS SCHEMAS
# ============================================================================

class HealthStatus(BaseModel):
    """System health status."""
    
    status: str = Field(..., description="healthy, degraded, unhealthy")
    version: str
    timestamp: datetime
    components: dict[str, dict[str, Any]]


class ErrorResponse(BaseModel):
    """Standard error response."""
    
    error: str
    message: str
    details: Optional[dict[str, Any]] = None
    request_id: Optional[str] = None
