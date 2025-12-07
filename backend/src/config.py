"""
Configuration module using Pydantic Settings.
Loads environment variables for the AI Career Coach backend.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI SDK Configuration (compatible with OpenRouter, Ollama, or OpenAI)
    # SECURITY: These must be set via environment variables - no hardcoded credentials
    openai_base_url: str = "https://openrouter.ai/api/v1"  # Default to OpenRouter
    openai_api_key: str = ""  # Required - set via environment
    openai_model: str = "openai/gpt-4o-mini"  # OpenRouter model format
    openai_embedding_model: str = "openai/text-embedding-3-small"
    openai_temperature: float = 0.3
    openai_max_tokens: int = 4096
    openai_timeout: int = 120  # 2 min for cloud APIs
    openai_fallback_model: str = "google/gemini-2.0-flash-exp:free"  # Fallback when primary fails

    # OpenRouter specific (optional - for rankings)
    openrouter_app_url: str = ""
    openrouter_app_name: str = "AI Career Coach"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = True

    # CORS Configuration
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # File Upload Configuration
    max_upload_size_mb: int = 10
    upload_temp_dir: str = "/tmp/career-coach"
    allowed_extensions: str = ".pdf,.docx,.txt"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    class Config:
        env_file = ".env"
        extra = "ignore"

    def get_allowed_origins_list(self) -> list[str]:
        """Get allowed origins as a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    def get_allowed_extensions_list(self) -> list[str]:
        """Get allowed file extensions as a list."""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
