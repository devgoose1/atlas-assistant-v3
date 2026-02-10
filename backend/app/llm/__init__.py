"""
LLM Provider Factory

Creates the appropriate LLM provider based on configuration.
"""

from typing import Optional
from .base import BaseLLMProvider, LLMResponse
from .ollama_provider import OllamaProvider
from .llamacpp_provider import LlamaCppProvider


def get_llm_provider(
    provider_type: str = "ollama",
    model_name: Optional[str] = None,
    base_url: Optional[str] = None,
    max_tokens: int = 256,
    temperature: float = 0.1
) -> BaseLLMProvider:
    """
    Factory function to create LLM provider.

    Args:
        provider_type: "ollama" or "llamacpp"
        model_name: Model name (provider-specific defaults if None)
        base_url: Base URL for the provider API
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature

    Returns:
        Configured LLM provider instance

    Raises:
        ValueError: If provider_type is not supported
    """
    if provider_type.lower() == "ollama":
        kwargs = {
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        if model_name:
            kwargs["model_name"] = model_name
        if base_url:
            kwargs["base_url"] = base_url
        return OllamaProvider(**kwargs)

    elif provider_type.lower() == "llamacpp":
        kwargs = {
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        if model_name:
            kwargs["model_name"] = model_name
        if base_url:
            kwargs["base_url"] = base_url
        return LlamaCppProvider(**kwargs)

    else:
        raise ValueError(f"Unsupported provider type: {provider_type}. Use 'ollama' or 'llamacpp'.")


__all__ = [
    "BaseLLMProvider",
    "OllamaProvider",
    "LlamaCppProvider",
    "LLMResponse",
    "get_llm_provider"
]
