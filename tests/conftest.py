from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app.core.settings import Settings, get_settings
from backend.app.main import app


@pytest.fixture(autouse=True)
def clear_settings_cache() -> Iterator[None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture()
def test_settings(tmp_path: Path) -> Settings:
    return Settings(
        temp_dir=tmp_path,
        llm_provider="none",
    )


@pytest.fixture()
def client(test_settings: Settings) -> TestClient:
    app.dependency_overrides[get_settings] = lambda: test_settings
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
