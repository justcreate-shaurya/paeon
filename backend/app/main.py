"""
Paeon AI Backend - Main Application

Production-grade FastAPI application for the Clinical Intelligence System.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import api_router
from app.core.config import settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    # Startup
    # Validate required external API keys early to fail fast with clear message
    if not settings.gemini_api_key:
        logger.error("Missing required API key: GEMINI_API_KEY", gemini_api_key_present=False)
        raise RuntimeError("GEMINI_API_KEY is not set. Set it in your environment or backend/.env before starting the server.")

    logger.info(
        "Starting Paeon AI",
        version=settings.app_version,
        environment=settings.environment,
    )
    
    yield
    
    # Shutdown
    logger.info("Shutting down Paeon AI")
    
    # Close any open connections
    from app.services.rag import rag_engine
    await rag_engine.close()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="""
# Paeon AI - Clinical-to-Vernacular Bridge

A regulated clinical intelligence system for Digital Medical Representatives.

## Core Capabilities

### 1. Slang-to-Clinical Translation
Transforms colloquial patient language from any supported language into 
structured clinical terminology with SNOMED-CT and ICD-10 codes.

### 2. Regulatory Intelligence (RAG)
Real-time access to drug intelligence from:
- FDA MedWatch (recalls)
- FDA Safety Alerts
- DailyMed (drug labels)
- PubMed (clinical evidence)

### 3. Fair Balance Asset Generation
Generates compliant patient education materials with:
- Balanced benefits and risks
- Black box warnings
- Required disclaimers
- PDF/PNG export

## Compliance

This system adheres to:
- **DPDP Act 2023** (India) data protection
- **Fair Balance** medical content guidelines
- **CDS** (Clinical Decision Support) regulations

## Important Disclaimers

⚠️ **For Healthcare Professional use only**

⚠️ **This is NOT a diagnostic tool**

⚠️ **The system does NOT prescribe treatments**

All medical decisions must be made by qualified healthcare providers.
    """,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing."""
    start_time = datetime.now(timezone.utc)
    
    response = await call_next(request)
    
    duration = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
    
    logger.info(
        "Request processed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=round(duration, 2),
    )
    
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    logger.error(
        "Unhandled exception",
        error=str(exc),
        path=request.url.path,
        method=request.method,
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred. Please try again.",
            "disclaimer": "For Healthcare Professional use only. Not a diagnostic tool.",
        },
    )


# Include API routes
app.include_router(api_router, prefix=settings.api_prefix)


# Root redirect
@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirect root to API docs."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
