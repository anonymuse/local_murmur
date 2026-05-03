from __future__ import annotations

from fastapi import FastAPI

from backend.app.api.router import api_router
from backend.app.core.logging import configure_logging
from backend.app.core.settings import get_settings

configure_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(api_router)
