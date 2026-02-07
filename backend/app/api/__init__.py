"""API router aggregation."""

from fastapi import APIRouter

from app.api.slang import router as slang_router
from app.api.rag import router as rag_router
from app.api.assets import router as assets_router
from app.api.health import router as health_router

api_router = APIRouter()

# Include all routers
api_router.include_router(slang_router)
api_router.include_router(rag_router)
api_router.include_router(assets_router)
api_router.include_router(health_router)
