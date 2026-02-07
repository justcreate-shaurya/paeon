"""
Paeon AI Backend - Core Configuration

Production-grade settings management using pydantic-settings.
All sensitive values loaded from environment variables.
"""

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable loading."""

    model_config = SettingsConfigDict(
        env_file=[".env", "backend/.env"],
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Paeon AI"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"

    # API
    api_prefix: str = "/api/v1"
    cors_origins: List[str] = Field(default=["http://localhost:5173", "http://localhost:3000"])

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            import json
            return json.loads(v)
        return v

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://paeon:paeon@localhost:5432/paeon_db"
    )

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Vector Database
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "paeon_medical_docs"

    # Google Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3-flash"
    gemini_embedding_model: str = "embedding-001"

    # Security
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # External APIs
    fda_api_key: str = ""
    pubmed_api_key: str = ""

    # Object Storage
    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "paeon-assets"

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # Monitoring
    sentry_dsn: str = ""
    prometheus_enabled: bool = True

    # Compliance
    audit_log_retention_days: int = 2555  # ~7 years
    pii_detection_enabled: bool = True
    fair_balance_strict_mode: bool = True


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance for dependency injection."""
    return Settings()


settings = get_settings()
