from __future__ import annotations

import pytest

from backend.app.core.settings import Settings


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.app_name == "Local Murmur"
    assert settings.app_port == 8000
    assert "wav" in settings.supported_audio_extensions
    assert settings.ollama_base_url.startswith("http://")
    assert settings.max_upload_size_bytes == settings.max_upload_size_mb * 1024 * 1024


def test_settings_rejects_invalid_port() -> None:
    with pytest.raises(ValueError):
        Settings(app_port=0)


def test_settings_rejects_openai_without_key() -> None:
    with pytest.raises(ValueError):
        Settings(llm_provider="openai", openai_model="gpt-4.1-mini")


def test_settings_rejects_ollama_without_model() -> None:
    with pytest.raises(ValueError):
        Settings(ollama_model="", llm_provider="ollama")
