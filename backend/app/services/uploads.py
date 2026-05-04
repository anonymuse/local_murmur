from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from backend.app.core.settings import Settings
from backend.app.core.tempfiles import cleanup_path, get_temp_root, stage_upload_bytes


@dataclass(slots=True)
class StagedUpload:
    path: Path
    filename: str
    content_type: str | None
    size_bytes: int


def validate_upload_filename(filename: str | None, supported_extensions: tuple[str, ...]) -> str:
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A filename is required for upload intake.",
        )

    suffix = Path(filename).suffix.lower().lstrip(".")
    if suffix not in supported_extensions:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported audio format: {suffix or 'unknown'}",
        )
    return suffix


def validate_upload_content_type(
    *,
    filename: str,
    content_type: str | None,
) -> None:
    extension = Path(filename).suffix.lower().lstrip(".")
    expected_content_types: dict[str, tuple[str, ...]] = {
        "wav": ("audio/wav", "audio/x-wav", "audio/wave", "audio/vnd.wave"),
        "m4a": ("audio/mp4", "audio/x-m4a", "audio/m4a"),
        "aac": ("audio/aac", "audio/x-aac", "audio/mp4"),
        "mp3": ("audio/mpeg", "audio/mp3"),
        "flac": ("audio/flac", "audio/x-flac"),
        "ogg": ("audio/ogg", "application/ogg"),
        "webm": ("audio/webm", "video/webm"),
        "mp4": ("audio/mp4", "video/mp4"),
    }
    allowed = expected_content_types.get(extension)
    if allowed is None:
        return
    if content_type is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Audio uploads must include a content type.",
        )
    if content_type.lower() not in allowed:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported audio content type for .{extension} upload.",
        )


def validate_upload_size(*, size_bytes: int, max_upload_size_bytes: int) -> None:
    if size_bytes > max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="Uploaded audio exceeds the configured maximum size.",
        )


async def stage_upload(
    *,
    upload: UploadFile,
    settings: Settings,
) -> StagedUpload:
    contents = await upload.read()
    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded audio file is empty.",
        )
    validate_upload_size(size_bytes=len(contents), max_upload_size_bytes=settings.max_upload_size_bytes or 0)

    root = get_temp_root(settings.temp_dir)
    path = stage_upload_bytes(
        root=root,
        filename=upload.filename or "audio.upload",
        contents=contents,
    )
    return StagedUpload(
        path=path,
        filename=upload.filename or "audio.upload",
        content_type=upload.content_type,
        size_bytes=len(contents),
    )


def cleanup_staged_upload(staged_upload: StagedUpload | None) -> None:
    if staged_upload is None:
        return
    cleanup_path(staged_upload.path)
