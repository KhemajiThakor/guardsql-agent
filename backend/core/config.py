from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    ollama_base_url: str
    ollama_model: str
    ollama_timeout: int = 60
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"
    auth_enabled: bool = False
    auth_username: str = "admin"
    auth_password: str = "changeme"

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()
