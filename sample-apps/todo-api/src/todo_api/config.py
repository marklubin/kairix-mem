import os
from pathlib import Path
from typing import List, Optional, Set

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.
    
    Loads from environment variables and/or .env file.
    """
    
    # App settings
    APP_NAME: str = "Todo API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str = Field(
        "sqlite+aiosqlite:///./todo.db",
        description="SQLAlchemy database connection string",
    )
    SQL_ECHO: bool = False
    
    # Security settings
    API_KEYS: Set[str] = Field(
        {"test_key"}, description="Set of valid API keys"
    )
    
    # Path settings
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


# Create settings instance
settings = Settings()

# Create directory for SQLite DB if using file-based SQLite
if settings.DATABASE_URL.startswith("sqlite+aiosqlite:///./"):
    db_path = settings.BASE_DIR / settings.DATABASE_URL.split("///./")[1]
    db_dir = db_path.parent
    db_dir.mkdir(exist_ok=True, parents=True)