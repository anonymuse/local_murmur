from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile

from backend.app.core.settings import Settings, get_settings
from backend.app.schemas.transcribe import TranscribeIntakeResponse
from backend.app.services.uploads import (
    cleanup_staged_upload,
    stage_upload,
    validate_upload_content_type,
    validate_upload_filename,
)

router = APIRouter(tags=["transcribe"])


@router.post("/transcribe", response_model=TranscribeIntakeResponse, status_code=202)
async def transcribe(
    upload: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
) -> TranscribeIntakeResponse:
    validate_upload_filename(upload.filename, settings.supported_audio_extensions)
    validate_upload_content_type(filename=upload.filename or "", content_type=upload.content_type)
    staged_upload = None
    try:
        staged_upload = await stage_upload(upload=upload, settings=settings)
        return TranscribeIntakeResponse(
            filename=staged_upload.filename,
            content_type=staged_upload.content_type,
            size_bytes=staged_upload.size_bytes,
        )
    finally:
        cleanup_staged_upload(staged_upload)
        await upload.close()
