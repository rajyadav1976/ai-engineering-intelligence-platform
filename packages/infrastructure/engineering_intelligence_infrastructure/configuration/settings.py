from __future__ import annotations

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Application
    app_env: str = "local"
    app_name: str = "ai-engineering-intelligence-platform"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_database: str = "engineering_intelligence"
    postgres_user: str = "engineering_intelligence"
    postgres_password: str = "change-me"

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    # LLM
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "qwen3"

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("ollama_host")
    @classmethod
    def validate_ollama_host(cls, value: str) -> str:
        """Validate and normalize the Ollama base URL."""
        value = value.rstrip("/")

        if not value.startswith(("http://", "https://")):
            raise ValueError(
                "ollama_host must start with http:// or https://"
            )

        return value

    @field_validator("ollama_model")
    @classmethod
    def validate_ollama_model(cls, value: str) -> str:
        """Validate the configured default Ollama model."""
        value = value.strip()

        if not value:
            raise ValueError("ollama_model cannot be empty")

        return value


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()