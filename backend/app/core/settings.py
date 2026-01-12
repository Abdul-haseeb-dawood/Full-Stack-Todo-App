from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str
    environment: str = "development"
    log_level: str = "info"

    class Config:
        env_file = ".env"


settings = Settings()