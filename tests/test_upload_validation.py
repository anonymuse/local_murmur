from __future__ import annotations

from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from backend.app.core.settings import Settings, get_settings
from backend.app.main import app


def test_transcribe_accepts_supported_wav_upload(client) -> None:
    response = client.post(
        "/transcribe",
        files={"upload": ("sample.wav", BytesIO(b"fake-wav-data"), "audio/wav")},
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["status"] == "accepted"
    assert payload["asr_status"] == "not_implemented"
    assert payload["message"] == "ASR not implemented yet"
    assert payload["filename"] == "sample.wav"
    assert payload["content_type"] == "audio/wav"
    assert payload["size_bytes"] == len(b"fake-wav-data")
    assert "path" not in payload


@pytest.mark.parametrize(
    ("filename", "content_type"),
    [
        ("sample.wav", "audio/wav"),
        ("sample.m4a", "audio/mp4"),
        ("sample.aac", "audio/aac"),
        ("sample.mp3", "audio/mpeg"),
    ],
)
def test_transcribe_accepts_explicit_mvp_formats(client, filename: str, content_type: str) -> None:
    response = client.post(
        "/transcribe",
        files={"upload": (filename, BytesIO(b"data"), content_type)},
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
