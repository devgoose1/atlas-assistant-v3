"""
Command Router Service

Routes classified intents to appropriate handlers.
Provides deterministic responses for common commands.
"""

from datetime import datetime
from typing import Dict, Any
from .intent_classifier import IntentType
from ..llm import BaseLLMProvider, LLMResponse


class CommandRouter:
    """
    Routes intents to appropriate handlers.

    For deterministic commands (time, greetings), returns direct responses.
    For open-ended queries, uses LLM to generate responses.
    """

    def __init__(self, llm_provider: BaseLLMProvider):
        """
        Initialize command router.

        Args:
            llm_provider: LLM provider instance
        """
        self.llm = llm_provider

    def route(self, intent: str, entities: Dict[str, Any], user_input: str) -> str:
        """
        Route intent to appropriate handler.

        Args:
            intent: Classified intent type
            entities: Extracted entities
            user_input: Original user input

        Returns:
            Response text
        """
        intent_type = IntentType(intent) if isinstance(intent, str) else intent

        # Route to specific handlers
        if intent_type == IntentType.GREETING:
            return self._handle_greeting()

        elif intent_type == IntentType.TIME:
            return self._handle_time()

        elif intent_type == IntentType.WEATHER:
            return self._handle_weather(entities)

        elif intent_type == IntentType.CALCULATION:
            return self._handle_calculation(user_input)

        elif intent_type == IntentType.TIMER:
            return self._handle_timer(entities)

        elif intent_type == IntentType.REMINDER:
            return self._handle_reminder(entities)

        elif intent_type in [IntentType.QUESTION, IntentType.GENERAL]:
            return self._handle_general_query(user_input)

        else:
            return "I'm not sure how to help with that. Could you rephrase?"

    def _handle_greeting(self) -> str:
        """Handle greeting intent."""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        return f"{greeting}! I'm JARVIS. How can I assist you?"

    def _handle_time(self) -> str:
        """Handle time query."""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d, %Y")
        return f"It's currently {time_str} on {date_str}."

    def _handle_weather(self, entities: Dict[str, Any]) -> str:
        """
        Handle weather query.

        Note: This is a placeholder. In production, integrate with a weather API.
        """
        location = entities.get("location", "your location")
        return f"I don't have access to weather data yet. Weather integration for {location} is coming soon."

    def _handle_calculation(self, user_input: str) -> str:
        """
        Handle calculation request.

        Note: For safety, use the LLM to interpret the calculation
        rather than using eval() on user input.
        """
        prompt = f"Calculate and respond with just the result: {user_input}"
        response = self.llm.generate(
            prompt=prompt,
            system_prompt="You are a calculator. Respond only with the numerical result.",
            max_tokens=64,
            temperature=0.0
        )

        if response.error:
            return "I couldn't perform that calculation."

        return f"The result is: {response.text.strip()}"

    def _handle_timer(self, entities: Dict[str, Any]) -> str:
        """
        Handle timer request.

        Note: This is a placeholder. Timer functionality requires
        persistent state or background tasks.
        """
        duration = entities.get("duration", "the specified time")
        return f"Timer functionality is not yet implemented. Timer for {duration} requested."

    def _handle_reminder(self, entities: Dict[str, Any]) -> str:
        """
        Handle reminder request.

        Note: This is a placeholder. Reminder functionality requires
        persistent state or a task queue.
        """
        return "Reminder functionality is not yet implemented."

    def _handle_general_query(self, user_input: str) -> str:
        """
        Handle general questions using LLM.

        Keep prompts simple for small models.
        """
        system_prompt = "You are JARVIS, a helpful assistant. Answer briefly and directly."

        response = self.llm.generate(
            prompt=user_input,
            system_prompt=system_prompt,
            max_tokens=256,
            temperature=0.3
        )

        if response.error:
            return "I'm having trouble processing that request right now."

        return response.text.strip()
