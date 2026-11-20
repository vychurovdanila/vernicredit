# -*- coding: utf-8 -*-
"""Application settings loaded from environment variables / .env file.

Security rules (Makefab):
- No hardcoded secrets and no default values for required secrets.
- The application must fail fast on startup when a required variable is missing.
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the API.

    Values are read from environment variables first, then from `backend/.env`.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- Database -----------------------------------------------------------
    DATABASE_URL: str = "sqlite:///./vernicredit.db"

    # --- JWT / security -----------------------------------------------------
    # No default on purpose: missing SECRET_KEY must raise during startup.
    SECRET_KEY: str = Field(..., min_length=8)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- CORS ---------------------------------------------------------------
    # Comma-separated origins, e.g. "http://localhost:5173,http://localhost:3000".
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    @field_validator("SECRET_KEY")
    @classmethod
    def _secret_key_must_not_be_placeholder(cls, value: str) -> str:
        """Reject empty values and the sample placeholder from .env.example."""
        cleaned = value.strip()
        if not cleaned or cleaned == "your-secret-key-here":
            raise ValueError(
                "SECRET_KEY is not configured. Set a strong value in backend/.env "
                "(generate with: openssl rand -hex 32)."
            )
        return cleaned

    @property
    def cors_origins(self) -> list[str]:
        """Return ALLOWED_ORIGINS as a list, dropping blanks and wildcards."""
        origins = [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
        return [origin for origin in origins if origin and origin != "*"]


settings = Settings()
