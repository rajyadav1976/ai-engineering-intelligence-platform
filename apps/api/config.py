from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Engineering Intelligence API"
    app_env: str = "local"

    api_host: str = "localhost"
    api_port: int = 8000

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgress_database: str = "engineering_intelligence"
    postgres_user: str = "engineering_intelligence"
    postgres_password: str = "postgres"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    ollama_host: str = "localhost"
    ollama_model: str = "qwen3"

    log_level: str = "info"

    model_config = SettingsConfigDict(env_file=".env", 
                                      env_file_encoding="utf-8",
                                      casesensitive=False)
