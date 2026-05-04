from __future__ import annotations

from io import BytesIO
import wave

import pytest
from fastapi.testclient import TestClient

from backend.app.core.settings import Settings, get_settings
from backend.app.main import app


def make_wav_bytes(*, duration_seconds: float = 1.0, frame_rate: int = 16000) -> bytes:
    buffer = BytesIO()
    frame_count = int(duration_seconds * frame_rate)
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(frame_rate)
        wav_file.writeframes(b"\x00\x00" * frame_count)
    return buffer.getvalue()


def test_transcribe_accepts_supported_wav_upload(client) -> None:
    response = client.post(
        "/transcribe",
        files={"upload": ("sample.wav", BytesIO(make_wav_bytes()), "audio/wav")},
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["status"] == "accepted"
    assert payload["asr_status"] == "not_implemented"
    assert payload["message"] == "ASR not implemented yet"
    assert payload["filename"] == "sample.wav"
    assert payload["content_type"] == "audio/wav"
    assert payload["size_bytes"] == len(make_wav_bytes())
    assert payload["duration_seconds"] == pytest.approx(1.0, rel=1e-3)
    assert "path" not in payload


@pytest.mark.parametrize(
    ("filename", "content_type", "payload"),
    [
        ("sample.wav", "audio/wav", make_wav_bytes()),
        ("sample.m4a", "audio/mp4", b"data"),
        ("sample.aac", "audio/aac", b"data"),
        ("sample.mp3", "audio/mpeg", b"data"),
    ],
)
def test_transcribe_accepts_explicit_mvp_formats(
    client,
    filename: str,
    content_type: str,
    payload: bytes,
) -> None:
    response = client.post(
        "/transcribe",
        files={"upload": (filename, BytesIO(payload), content_type)},
    )
    assert response.status_code == 202


def test_transcribe_rejects_unsupported_format(client) -> None:
    response = client.post(
        "/transcribe",
        files={"upload": ("sample.txt", BytesIO(b"not-audio"), "text/plain")},
    )
    assert response.status_code == 415


def test_transcribe_rejects_missing_filename(client) -> None:
    response = client.post(
        "/transcribe",
        files={"upload": ("", BytesIO(b"data"), "audio/wav")},
    )
    assert response.status_code == 422


def test_transcribe_rejects_extension_content_type_mismatch(client) -> None:
    response = client.post(
        "/transcribe",
        files={"upload": ("sample.wav", BytesIO(b"data"), "audio/mp4")},
    )
    assert response.status_code == 415


def test_transcribe_rejects_missing_content_type(client) -> None:
    response = client.post(
        "/transcribe",
        files={"upload": ("sample.wav", BytesIO(b"data"), "application/octet-stream")},
    )
    assert response.status_code == 415


def test_transcribe_enforces_max_upload_size(tmp_path) -> None:
    settings = Settings(
        temp_dir=tmp_path,
        llm_provider="none",
        max_upload_size_mb=1,
    )
    app.dependency_overrides[get_settings] = lambda: settings
    try:
        client = TestClient(app)
        response = client.post(
            "/transcribe",
            files={"upload": ("sample.wav", BytesIO(b"x" * (settings.max_upload_size_bytes + 1)), "audio/wav")},
        )
        assert response.status_code == 413
    finally:
        app.dependency_overrides.clear()


def test_transcribe_rejects_invalid_wav_container(client) -> None:
    response = client.post(
        "/transcribe",
        files={"upload": ("sample.wav", BytesIO(b"not-a-real-wav"), "audio/wav")},
    )
    assert response.status_code == 415


def test_transcribe_rejects_wav_longer_than_max_duration(tmp_path) -> None:
    settings = Settings(
        temp_dir=tmp_path,
        llm_provider="none",
        max_audio_duration_seconds=1,
    )
    app.dependency_overrides[get_settings] = lambda: settings
    try:
        client = TestClient(app)
        response = client.post(
            "/transcribe",
            files={
                "upload": (
                    "sample.wav",
                    BytesIO(make_wav_bytes(duration_seconds=2.0)),
                    "audio/wav",
                )
            },
        )
        assert response.status_code == 413
    finally:
        app.dependency_overrides.clear()


def test_transcribe_returns_null_duration_for_non_wav(client) -> None:
    response = client.post(
        "/transcribe",
        files={"upload": ("sample.mp3", BytesIO(b"data"), "audio/mpeg")},
    )
    assert response.status_code == 202
    assert response.json()["duration_seconds"] is None
