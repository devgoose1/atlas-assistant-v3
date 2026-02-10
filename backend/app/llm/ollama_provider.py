"""
Ollama LLM Provider

Uses Ollama API for local LLM inference.
Suitable for development environments.
"""

import requests
from typing import Optional
from .base import BaseLLMProvider, LLMResponse


class OllamaProvider(BaseLLMProvider):
    """
    Ollama API provider for local LLM inference.

    Connects to Ollama server running locally or on network.
    """

    def __init__(
        self,
        model_name: str = "qwen:1.5b-chat-v1.5-q4_0",
        base_url: str = "http://localhost:11434",
        max_tokens: int = 256,
        temperature: float = 0.1
    ):
        """
        Initialize Ollama provider.

        Args:
            model_name: Ollama model name
            base_url: Ollama API base URL
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
        """
        super().__init__(model_name, max_tokens, temperature)
        self.base_url = base_url.rstrip("/")
        self.generate_url = f"{self.base_url}/api/generate"
        self.chat_url = f"{self.base_url}/api/chat"

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        json_mode: bool = False
    ) -> LLMResponse:
        """Generate text using Ollama API."""
        try:
            # Use chat endpoint if system prompt provided
            if system_prompt:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
                payload = {
                    "model": self.model_name,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens or self.max_tokens,
                        "temperature": temperature if temperature is not None else self.temperature,
                    }
                }
                if json_mode:
                    payload["format"] = "json"

                response = requests.post(self.chat_url, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()

                return LLMResponse(
                    text=data["message"]["content"],
                    tokens_used=data.get("eval_count"),
                    model=self.model_name
                )
            else:
                # Use generate endpoint for simple prompts
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens or self.max_tokens,
                        "temperature": temperature if temperature is not None else self.temperature,
                    }
                }
                if json_mode:
                    payload["format"] = "json"

                response = requests.post(self.generate_url, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()

                return LLMResponse(
                    text=data["response"],
                    tokens_used=data.get("eval_count"),
                    model=self.model_name
                )

        except requests.RequestException as e:
            return LLMResponse(
                text="",
                error=f"Ollama API error: {str(e)}",
                model=self.model_name
            )
        except Exception as e:
            return LLMResponse(
                text="",
                error=f"Unexpected error: {str(e)}",
                model=self.model_name
            )

    def health_check(self) -> bool:
        """Check if Ollama is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
