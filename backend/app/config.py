"""
Configuration Management

Loads configuration from environment variables with sensible defaults.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Create a .env file in the backend directory to override defaults.
    """

    # API Settings
    app_name: str = "JARVIS Assistant"
    app_version: str = "1.0.0"
    host: str = "0.0.0.0"  # Bind to all interfaces for network access
    port: int = 8000
    debug: bool = False
    cors_origins: str = "*"  # Comma-separated origins, or "*" for all

    # LLM Provider Settings
    llm_provider: str = "ollama"  # "ollama" or "llamacpp"
    llm_model_name: Optional[str] = None  # Provider-specific model name
    llm_base_url: Optional[str] = None  # Provider API URL
    llm_max_tokens: int = 256  # Keep low for resource constraints
    llm_temperature: float = 0.1  # Low temperature for deterministic outputs

    # Performance Settings
    request_timeout: int = 30  # Timeout for LLM requests in seconds
    max_context_length: int = 1500  # Leave headroom below 2048 token limit

    # Feature Flags
    enable_command_routing: bool = True
    enable_intent_classification: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings
