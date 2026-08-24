from __future__ import annotations

import pytest

from engineering_intelligence_infrastructure.configuration import (
    Settings,
)


def test_application_settings_loads_environment_configuration() -> None:
    settings = Settings()

    assert settings.ollama_host == "http://localhost:11434"
    assert settings.ollama_model == "qwen3"
    assert settings.qdrant_host == "localhost"
    assert settings.qdrant_port == 6333
    assert settings.postgres_database == "engineering_intelligence"
    assert settings.postgres_user == "engineering_intelligence"
    assert settings.postgres_password == "engineering_intelligence_dev"

def test_ollama_configuration_is_loaded() -> None:
    settings = Settings()

    assert settings.ollama_host == "http://localhost:11434"
    assert settings.ollama_model == "qwen3"


def test_ollama_host_must_be_http_url() -> None:
    with pytest.raises(ValueError):
        Settings(ollama_host="localhost:11434")


def test_ollama_model_cannot_be_empty() -> None:
    with pytest.raises(ValueError):
        Settings(ollama_model="   ")
    