"""
Paeon AI Backend - Database Models

SQLAlchemy ORM models for the clinical intelligence system.
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# ============================================================================
# USER & SESSION MODELS
# ============================================================================

class User(Base, TimestampMixin):
    """Healthcare professional user accounts."""
    
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="clinician")
    organization: Mapped[str | None] = mapped_column(String(255))
    license_number: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    translations: Mapped[list["TranslationQuery"]] = relationship(back_populates="user")
    assets: Mapped[list["PatientAsset"]] = relationship(back_populates="created_by_user")


# ============================================================================
# SLANG-TO-CLINICAL TRANSLATION MODELS
# ============================================================================

class TranslationQuery(Base, TimestampMixin):
    """Records of patient language translation queries."""
    
    __tablename__ = "translation_queries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), index=True
    )
    
    # Input data (PII-stripped)
    raw_input: Mapped[str] = mapped_column(Text, nullable=False)
    detected_language: Mapped[str] = mapped_column(String(50))
    normalized_english: Mapped[str] = mapped_column(Text)
    
    # Clinical output
    clinical_interpretation: Mapped[str] = mapped_column(Text)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    rationale: Mapped[str] = mapped_column(Text)
    
    # Standard codes
    standard_codes: Mapped[dict[str, Any]] = mapped_column(JSON, default=list)
    
    # Clinician feedback
    clinician_approved: Mapped[bool | None] = mapped_column(Boolean)
    clinician_edited: Mapped[bool] = mapped_column(Boolean, default=False)
    clinician_correction: Mapped[str | None] = mapped_column(Text)
    
    # Audit
    session_id: Mapped[str | None] = mapped_column(String(64), index=True)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="translations")

    __table_args__ = (
        Index("ix_translation_queries_created_at", "created_at"),
        Index("ix_translation_queries_language", "detected_language"),
    )


class ClinicalMapping(Base, TimestampMixin):
    """Curated clinical mappings for common colloquial expressions."""
    
    __tablename__ = "clinical_mappings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    
    # Source expression
    colloquial_expression: Mapped[str] = mapped_column(Text, nullable=False)
    source_language: Mapped[str] = mapped_column(String(50), default="en")
    
    # Clinical mapping
    clinical_term: Mapped[str] = mapped_column(String(500), nullable=False)
    snomed_code: Mapped[str | None] = mapped_column(String(50))
    icd10_code: Mapped[str | None] = mapped_column(String(50))
    umls_cui: Mapped[str | None] = mapped_column(String(50))
    
    # Metadata
    body_system: Mapped[str | None] = mapped_column(String(100))
    severity_hint: Mapped[str | None] = mapped_column(String(50))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_by: Mapped[str | None] = mapped_column(String(255))
    usage_count: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        Index("ix_clinical_mappings_expression", "colloquial_expression"),
        Index("ix_clinical_mappings_snomed", "snomed_code"),
    )


# ============================================================================
# DRUG INTELLIGENCE MODELS
# ============================================================================

class DrugIntelligence(Base, TimestampMixin):
    """Regulatory intelligence about drugs from FDA, DailyMed, etc."""
    
    __tablename__ = "drug_intelligence"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    
    # Drug identification
    drug_name: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    ndc_codes: Mapped[list[str]] = mapped_column(JSON, default=list)
    rxcui: Mapped[str | None] = mapped_column(String(50))
    
    # Intelligence type
    intel_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # recall, safety_alert, new_indication, label_update
    severity: Mapped[str] = mapped_column(String(20))  # high, medium, low, info
    
    # Content
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    full_content: Mapped[str | None] = mapped_column(Text)
    
    # Source verification
    source_name: Mapped[str] = mapped_column(String(100), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(1000))
    source_document_id: Mapped[str | None] = mapped_column(String(100))
    published_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    retrieved_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_hash: Mapped[str | None] = mapped_column(String(64))
    
    # Vector embedding ID (for RAG)
    embedding_id: Mapped[str | None] = mapped_column(String(100))

    __table_args__ = (
        Index("ix_drug_intelligence_drug_type", "drug_name", "intel_type"),
        Index("ix_drug_intelligence_published", "published_date"),
        Index("ix_drug_intelligence_severity", "severity"),
    )


class DrugLabel(Base, TimestampMixin):
    """Structured drug label information from DailyMed."""
    
    __tablename__ = "drug_labels"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    
    # Drug identification
    drug_name: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    generic_name: Mapped[str | None] = mapped_column(String(500))
    manufacturer: Mapped[str | None] = mapped_column(String(500))
    ndc_code: Mapped[str | None] = mapped_column(String(50))
    set_id: Mapped[str | None] = mapped_column(String(100), unique=True)
    
    # Label sections
    indications: Mapped[str | None] = mapped_column(Text)
    dosage_administration: Mapped[str | None] = mapped_column(Text)
    contraindications: Mapped[str | None] = mapped_column(Text)
    warnings_precautions: Mapped[str | None] = mapped_column(Text)
    adverse_reactions: Mapped[str | None] = mapped_column(Text)
    drug_interactions: Mapped[str | None] = mapped_column(Text)
    black_box_warning: Mapped[str | None] = mapped_column(Text)
    
    # Structured data
    dosage_forms: Mapped[list[str]] = mapped_column(JSON, default=list)
    routes: Mapped[list[str]] = mapped_column(JSON, default=list)
    
    # Source
    source_url: Mapped[str | None] = mapped_column(String(1000))
    effective_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_drug_labels_generic", "generic_name"),
    )


# ============================================================================
# PATIENT ASSET MODELS
# ============================================================================

class PatientAsset(Base, TimestampMixin):
    """Generated patient education assets."""
    
    __tablename__ = "patient_assets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    
    # Asset content
    drug_name: Mapped[str] = mapped_column(String(500), nullable=False)
    drug_dosage: Mapped[str | None] = mapped_column(String(100))
    
    # Structured content
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    how_to_take: Mapped[str] = mapped_column(Text)
    key_benefits: Mapped[list[str]] = mapped_column(JSON, default=list)
    safety_information: Mapped[str] = mapped_column(Text)
    contraindications: Mapped[list[str]] = mapped_column(JSON, default=list)
    black_box_warning: Mapped[str | None] = mapped_column(Text)
    disclaimer: Mapped[str] = mapped_column(Text)
    
    # Fair Balance compliance
    fair_balance_score: Mapped[float] = mapped_column(Float)
    compliance_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    compliance_notes: Mapped[str | None] = mapped_column(Text)
    
    # Export info
    pdf_url: Mapped[str | None] = mapped_column(String(1000))
    png_url: Mapped[str | None] = mapped_column(String(1000))
    export_count: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    created_by_user: Mapped["User"] = relationship(back_populates="assets")

    __table_args__ = (
        Index("ix_patient_assets_drug", "drug_name"),
        Index("ix_patient_assets_created", "created_at"),
    )


# ============================================================================
# AUDIT & COMPLIANCE MODELS
# ============================================================================

class AuditLog(Base):
    """Immutable audit log for compliance tracking."""
    
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    
    # Actor (anonymized)
    actor_id_hash: Mapped[str] = mapped_column(String(64), index=True)
    actor_role: Mapped[str | None] = mapped_column(String(50))
    
    # Action
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100))
    resource_id: Mapped[str | None] = mapped_column(String(100))
    
    # Context
    input_hash: Mapped[str | None] = mapped_column(String(64))
    output_hash: Mapped[str | None] = mapped_column(String(64))
    confidence_score: Mapped[float | None] = mapped_column(Float)
    
    # Compliance flags
    pii_detected: Mapped[bool] = mapped_column(Boolean, default=False)
    pii_stripped: Mapped[bool] = mapped_column(Boolean, default=False)
    safety_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    
    # Request metadata
    ip_address_hash: Mapped[str | None] = mapped_column(String(64))
    user_agent_hash: Mapped[str | None] = mapped_column(String(64))
    session_id: Mapped[str | None] = mapped_column(String(64))

    __table_args__ = (
        Index("ix_audit_logs_timestamp", "timestamp"),
        Index("ix_audit_logs_action", "action_type"),
        Index("ix_audit_logs_actor", "actor_id_hash"),
    )


class PIIDetectionLog(Base):
    """Log of detected and stripped PII for compliance verification."""
    
    __tablename__ = "pii_detection_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    
    # Reference
    query_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("translation_queries.id")
    )
    
    # Detection details (no actual PII stored)
    pii_types_detected: Mapped[list[str]] = mapped_column(JSON, default=list)
    pii_count: Mapped[int] = mapped_column(Integer, default=0)
    original_length: Mapped[int] = mapped_column(Integer)
    stripped_length: Mapped[int] = mapped_column(Integer)
    
    # Verification
    detection_model_version: Mapped[str] = mapped_column(String(50))
    confidence_scores: Mapped[dict[str, float]] = mapped_column(JSON, default=dict)

    __table_args__ = (
        Index("ix_pii_detection_timestamp", "timestamp"),
    )
