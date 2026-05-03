from __future__ import annotations

from fastapi import APIRouter

from backend.app.api.health import router as health_router
from backend.app.api.transcribe import router as transcribe_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(transcribe_router)
