"""
core/config.py
App-wide configuration loaded from environment variables.
"""

from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_timeout: int = 60  # seconds per request
    ollama_max_retries: int = 2

    # GitHub
    github_api_token: str = ""  # Optional — increases rate limit to 5000/hr

    # Analysis thresholds
    high_impact_threshold: float = 70.0   # PageRank score > this = high impact
    hot_zone_threshold: float = 65.0      # Composite score > this = hot zone

    # Cache directories (relative to backend/)
    summary_cache_dir: str = "./cache/summaries"
    audio_cache_dir: str = "./cache/audio"

    # CORS
    frontend_origin: str = "http://localhost:5173"

    # Ollama summary batch settings
    summary_batch_size: int = 5
    summary_batch_delay_ms: int = 500

    class Config:
        # Resolve .env relative to this file's directory (backend/) so it works
        # regardless of where uvicorn is launched from.
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"


_settings: "Settings | None" = None


def get_settings() -> "Settings":
    """Return the singleton settings instance, loaded from .env."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
