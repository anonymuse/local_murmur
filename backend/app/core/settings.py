from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.local-murmur",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Local Murmur"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    temp_dir: Path | None = None
    max_upload_size_mb: int = 25
    max_audio_duration_seconds: int = 300
    max_upload_size_bytes: int | None = None

    whisper_model: str = "large-v3-turbo"
    whisper_device: Literal["cpu", "cuda", "auto"] = "cuda"
    whisper_compute_type: Literal["float16", "float32", "int8", "int8_float16"] = (
        "float16"
    )

    llm_provider: Literal["none", "ollama", "openai"] = "ollama"
    ollama_base_url: str = "http://host.docker.internal:11434"
    ollama_model: str = "gemma4:e4b"
    openai_api_key: str = ""
    openai_model: str = ""

    supported_audio_extensions: tuple[str, ...] = Field(
        default=("wav", "m4a", "aac", "mp3", "flac", "ogg", "webm", "mp4"),
    )

    @field_validator("app_port", "max_upload_size_mb", "max_audio_duration_seconds")
    @classmethod
    def validate_positive_int(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("must be greater than zero")
        return value

    @field_validator("app_host", "whisper_model", "ollama_base_url", "ollama_model")
    @classmethod
    def validate_non_empty_string(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be empty")
        return value

    @field_validator("supported_audio_extensions")
    @classmethod
    def normalize_extensions(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(ext.lower().lstrip(".") for ext in value if ext.strip())
        if not normalized:
            raise ValueError("at least one supported audio extension is required")
        return normalized

    @model_validator(mode="after")
    def validate_provider_settings(self) -> "Settings":
        if self.llm_provider == "openai":
            if not self.openai_api_key.strip():
                raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
            if not self.openai_model.strip():
                raise ValueError("OPENAI_MODEL is required when LLM_PROVIDER=openai")
        if self.llm_provider == "ollama" and not self.ollama_model.strip():
            raise ValueError("OLLAMA_MODEL is required when LLM_PROVIDER=ollama")
        if self.max_upload_size_bytes is None:
            self.max_upload_size_bytes = self.max_upload_size_mb * 1024 * 1024
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
