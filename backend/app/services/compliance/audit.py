"""
Paeon AI - Audit Logging Service

Maintains immutable audit trail for regulatory compliance.
All operations are logged with anonymized identifiers.
"""

import hashlib
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import generate_anonymous_id
from app.db.models import AuditLog


class AuditService:
    """
    Compliance audit logging service.
    
    Logs all operations for regulatory review while
    maintaining user privacy through anonymization.
    """

    @staticmethod
    def hash_content(content: str) -> str:
        """Generate SHA-256 hash of content for audit purposes."""
        return hashlib.sha256(content.encode()).hexdigest()

    @staticmethod
    def hash_ip(ip_address: str | None, salt: str) -> str | None:
        """Hash IP address for privacy."""
        if not ip_address:
            return None
        return hashlib.sha256(f"{salt}:{ip_address}".encode()).hexdigest()[:32]

    async def log_translation(
        self,
        db: AsyncSession,
        user_id: str | None,
        input_text: str,
        output_text: str,
        confidence: float,
        pii_detected: bool,
        pii_stripped: bool,
        safety_flags: list[str],
        session_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        """Log a translation operation."""
        
        log_entry = AuditLog(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            actor_id_hash=generate_anonymous_id(user_id) if user_id else "anonymous",
            actor_role="clinician",
            action_type="slang_translation",
            resource_type="translation_query",
            input_hash=self.hash_content(input_text),
            output_hash=self.hash_content(output_text),
            confidence_score=confidence,
            pii_detected=pii_detected,
            pii_stripped=pii_stripped,
            safety_flags=safety_flags,
            session_id=session_id,
            ip_address_hash=self.hash_ip(ip_address, "paeon_audit"),
            user_agent_hash=self.hash_content(user_agent)[:32] if user_agent else None,
        )
        
        db.add(log_entry)
        await db.flush()
        
        return log_entry

    async def log_asset_generation(
        self,
        db: AsyncSession,
        user_id: str | None,
        drug_name: str,
        asset_id: str,
        fair_balance_score: float,
        compliance_verified: bool,
        session_id: str | None = None,
    ) -> AuditLog:
        """Log an asset generation operation."""
        
        log_entry = AuditLog(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            actor_id_hash=generate_anonymous_id(user_id) if user_id else "anonymous",
            actor_role="clinician",
            action_type="asset_generation",
            resource_type="patient_asset",
            resource_id=asset_id,
            input_hash=self.hash_content(drug_name),
            confidence_score=fair_balance_score,
            pii_detected=False,
            pii_stripped=False,
            safety_flags=[] if compliance_verified else ["fair_balance_warning"],
            session_id=session_id,
        )
        
        db.add(log_entry)
        await db.flush()
        
        return log_entry

    async def log_export(
        self,
        db: AsyncSession,
        user_id: str | None,
        asset_id: str,
        export_format: str,
        session_id: str | None = None,
    ) -> AuditLog:
        """Log an asset export operation."""
        
        log_entry = AuditLog(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            actor_id_hash=generate_anonymous_id(user_id) if user_id else "anonymous",
            actor_role="clinician",
            action_type=f"asset_export_{export_format}",
            resource_type="patient_asset",
            resource_id=asset_id,
            pii_detected=False,
            pii_stripped=False,
            safety_flags=[],
            session_id=session_id,
        )
        
        db.add(log_entry)
        await db.flush()
        
        return log_entry

    async def log_rag_query(
        self,
        db: AsyncSession,
        user_id: str | None,
        query: str,
        results_count: int,
        sources_verified: bool,
        session_id: str | None = None,
    ) -> AuditLog:
        """Log a RAG intelligence query."""
        
        log_entry = AuditLog(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            actor_id_hash=generate_anonymous_id(user_id) if user_id else "anonymous",
            actor_role="clinician",
            action_type="rag_query",
            resource_type="drug_intelligence",
            input_hash=self.hash_content(query),
            pii_detected=False,
            pii_stripped=False,
            safety_flags=[] if sources_verified else ["unverified_sources"],
            session_id=session_id,
        )
        
        db.add(log_entry)
        await db.flush()
        
        return log_entry

    async def get_logs(
        self,
        db: AsyncSession,
        actor_id: str | None = None,
        action_type: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> dict[str, Any]:
        """Retrieve audit logs with filtering."""
        from sqlalchemy import select, func
        
        query = select(AuditLog)
        count_query = select(func.count(AuditLog.id))
        
        if actor_id:
            actor_hash = generate_anonymous_id(actor_id)
            query = query.where(AuditLog.actor_id_hash == actor_hash)
            count_query = count_query.where(AuditLog.actor_id_hash == actor_hash)
        
        if action_type:
            query = query.where(AuditLog.action_type == action_type)
            count_query = count_query.where(AuditLog.action_type == action_type)
        
        if start_date:
            query = query.where(AuditLog.timestamp >= start_date)
            count_query = count_query.where(AuditLog.timestamp >= start_date)
        
        if end_date:
            query = query.where(AuditLog.timestamp <= end_date)
            count_query = count_query.where(AuditLog.timestamp <= end_date)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Get paginated results
        query = query.order_by(AuditLog.timestamp.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        result = await db.execute(query)
        entries = result.scalars().all()
        
        return {
            "entries": entries,
            "total": total,
            "page": page,
            "page_size": page_size,
        }


# Singleton instance
audit_service = AuditService()
