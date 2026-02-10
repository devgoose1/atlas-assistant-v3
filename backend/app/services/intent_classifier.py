"""
Intent Classification Service

Uses LLM to classify user intents and extract entities.
Designed for small, quantized models with limited context.
"""

import json
from typing import Dict, Any, Optional
from enum import Enum
from ..llm import BaseLLMProvider, LLMResponse


class IntentType(str, Enum):
    """Supported intent types."""
    GREETING = "greeting"
    QUESTION = "question"
    COMMAND = "command"
    WEATHER = "weather"
    TIME = "time"
    TIMER = "timer"
    REMINDER = "reminder"
    CALCULATION = "calculation"
    GENERAL = "general"
    UNKNOWN = "unknown"


# Minimal system prompt optimized for small models
INTENT_CLASSIFICATION_PROMPT = """You are a JSON-only assistant. Classify the user's intent and extract entities.

Intents: greeting, question, command, weather, time, timer, reminder, calculation, general, unknown

Output JSON only:
{"intent": "intent_type", "entities": {}, "confidence": 0.0-1.0}"""


class IntentClassifier:
    """
    Classifies user intents using LLM.

    Optimized for small models like Qwen 1.5B:
    - Short, structured prompts
    - JSON output format
    - Minimal examples
    """

    def __init__(self, llm_provider: BaseLLMProvider):
        """
        Initialize intent classifier.

        Args:
            llm_provider: LLM provider instance
        """
        self.llm = llm_provider

    def classify(self, user_input: str) -> Dict[str, Any]:
        """
        Classify user intent.

        Args:
            user_input: User's text input

        Returns:
            Dictionary with:
                - intent: IntentType
                - entities: Dict of extracted entities
                - confidence: Float between 0-1
                - raw_response: Optional raw LLM response
        """
        # Fallback for obvious patterns (avoid LLM call when possible)
        simple_intent = self._check_simple_patterns(user_input)
        if simple_intent:
            return simple_intent

        # Use LLM for classification
        prompt = f'User: "{user_input}"\n\nClassify:'

        response: LLMResponse = self.llm.generate(
            prompt=prompt,
            system_prompt=INTENT_CLASSIFICATION_PROMPT,
            max_tokens=128,  # Small output for JSON
            temperature=0.1,  # Deterministic
            json_mode=True
        )

        if response.error:
            return {
                "intent": IntentType.UNKNOWN,
                "entities": {},
                "confidence": 0.0,
                "error": response.error
            }

        try:
            # Parse JSON response
            result = json.loads(response.text)

            # Validate and normalize intent
            intent_str = result.get("intent", "unknown").lower()
            try:
                intent = IntentType(intent_str)
            except ValueError:
                intent = IntentType.UNKNOWN

            return {
                "intent": intent,
                "entities": result.get("entities", {}),
                "confidence": float(result.get("confidence", 0.5)),
                "raw_response": response.text
            }

        except json.JSONDecodeError:
            # LLM didn't return valid JSON
            return {
                "intent": IntentType.UNKNOWN,
                "entities": {},
                "confidence": 0.0,
                "error": "Invalid JSON from LLM",
                "raw_response": response.text
            }

    def _check_simple_patterns(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Check for simple patterns to avoid LLM calls.

        Args:
            user_input: User's text input

        Returns:
            Intent classification dict if pattern matched, None otherwise
        """
        text_lower = user_input.lower().strip()

        # Greetings
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        if any(text_lower.startswith(g) for g in greetings):
            return {
                "intent": IntentType.GREETING,
                "entities": {},
                "confidence": 1.0,
                "pattern_matched": True
            }

        # Time queries
        if any(phrase in text_lower for phrase in ["what time", "current time", "what's the time"]):
            return {
                "intent": IntentType.TIME,
                "entities": {},
                "confidence": 1.0,
                "pattern_matched": True
            }

        # Weather queries
        if any(phrase in text_lower for phrase in ["weather", "temperature", "forecast"]):
            return {
                "intent": IntentType.WEATHER,
                "entities": {},
                "confidence": 1.0,
                "pattern_matched": True
            }

        return None
