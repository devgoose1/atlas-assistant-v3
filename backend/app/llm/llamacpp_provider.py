"""
llama.cpp LLM Provider

Uses llama.cpp server for local LLM inference.
Optimized for production on Raspberry Pi 4.
"""

import requests
from typing import Optional
from .base import BaseLLMProvider, LLMResponse


class LlamaCppProvider(BaseLLMProvider):
    """
    llama.cpp server provider for local LLM inference.

    Connects to llama.cpp server running with --server flag.
    Optimized for resource-constrained environments.
    """

    def __init__(
        self,
        model_name: str = "qwen-1_5b-chat-q4_0.gguf",
        base_url: str = "http://localhost:8080",
        max_tokens: int = 256,
        temperature: float = 0.1
    ):
        """
        Initialize llama.cpp provider.

        Args:
            model_name: Model name (for logging only, model loaded at server start)
            base_url: llama.cpp server base URL
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
        """
        super().__init__(model_name, max_tokens, temperature)
        self.base_url = base_url.rstrip("/")
        self.completion_url = f"{self.base_url}/completion"
        self.health_url = f"{self.base_url}/health"

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        json_mode: bool = False
    ) -> LLMResponse:
        """Generate text using llama.cpp server."""
        try:
            # Combine system prompt and user prompt
            full_prompt = prompt
            if system_prompt:
                # Use Qwen chat template format
                full_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

            payload = {
                "prompt": full_prompt,
                "n_predict": max_tokens or self.max_tokens,
                "temperature": temperature if temperature is not None else self.temperature,
                "stop": ["<|im_end|>", "<|endoftext|>"],  # Stop tokens for Qwen
                "stream": False,
                # Optimizations for Raspberry Pi
                "cache_prompt": True,  # Cache prompts to save CPU
                "n_threads": 4,  # Use 4 cores on RPi4
            }

            if json_mode:
                # Guide model to output JSON
                payload["grammar"] = "root ::= object\nobject ::= \"{\" pair (\",\" pair)* \"}\"\npair ::= string \":\" value\nstring ::= \"\\\"\" [^\"]* \"\\\"\"\nvalue ::= string | number | object | array | \"true\" | \"false\" | \"null\"\narray ::= \"[\" value (\",\" value)* \"]\"\nnumber ::= \"-\"? [0-9]+ (\".\" [0-9]+)?"

            response = requests.post(self.completion_url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            return LLMResponse(
                text=data["content"].strip(),
                tokens_used=data.get("tokens_evaluated"),
                model=self.model_name
            )

        except requests.RequestException as e:
            return LLMResponse(
                text="",
                error=f"llama.cpp server error: {str(e)}",
                model=self.model_name
            )
        except Exception as e:
            return LLMResponse(
                text="",
                error=f"Unexpected error: {str(e)}",
                model=self.model_name
            )

    def health_check(self) -> bool:
        """Check if llama.cpp server is available."""
        try:
            response = requests.get(self.health_url, timeout=5)
            return response.status_code == 200
        except:
            return False
