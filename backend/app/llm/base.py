"""
LLM Provider Abstraction Layer

Provides a unified interface for different LLM backends (Ollama, llama.cpp).
Designed for resource-constrained environments like Raspberry Pi 4.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Standard response format from LLM providers."""
    text: str
    tokens_used: Optional[int] = None
    model: Optional[str] = None
    error: Optional[str] = None


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    All providers must implement generate() to ensure consistent interface
    regardless of the underlying LLM backend.
    """

    def __init__(self, model_name: str, max_tokens: int = 256, temperature: float = 0.1):
        """
        Initialize LLM provider.

        Args:
            model_name: Name or path to the model
            max_tokens: Maximum tokens to generate (keep low for resource constraints)
            temperature: Sampling temperature (low = more deterministic)
        """
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        json_mode: bool = False
    ) -> LLMResponse:
        """
        Generate text from the LLM.

        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            max_tokens: Override default max_tokens
            temperature: Override default temperature
            json_mode: Request JSON-formatted output

        Returns:
            LLMResponse with generated text and metadata
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Check if the LLM provider is available and responding.

        Returns:
            True if healthy, False otherwise
        """
        pass
