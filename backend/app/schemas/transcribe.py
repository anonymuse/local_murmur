from __future__ import annotations

from pydantic import BaseModel, Field


class TranscribeIntakeResponse(BaseModel):
    status: str = Field(default="accepted")
    asr_status: str = Field(default="not_implemented")
    message: str = Field(default="ASR not implemented yet")
    filename: str
    content_type: str | None = None
    size_bytes: int
    duration_seconds: float | None = None
