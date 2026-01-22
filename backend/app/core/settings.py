from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str
    gemini_api_key: Optional[str] = None
    backend_base_url: Optional[str] = "http://localhost:8000"
    environment: str = "development"
    log_level: str = "info"

    class Config:
        env_file = ".env"


settings = Settings()