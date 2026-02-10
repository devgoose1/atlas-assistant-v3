"""
Chat API Router

Handles chat requests and returns responses from JARVIS.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from ..config import get_settings, Settings
from ..llm import get_llm_provider, BaseLLMProvider
from ..services import IntentClassifier, CommandRouter


router = APIRouter(prefix="/api", tags=["chat"])


# Request/Response models
class ChatRequest(BaseModel):
    """Chat request from user."""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Optional context")


class ChatResponse(BaseModel):
    """Chat response from JARVIS."""
    response: str = Field(..., description="JARVIS response text")
    intent: Optional[str] = Field(default=None, description="Classified intent")
    confidence: Optional[float] = Field(default=None, description="Intent confidence")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


# Dependency to get LLM provider (singleton pattern)
_llm_provider_instance: Optional[BaseLLMProvider] = None


def get_llm_provider_instance(settings: Settings = Depends(get_settings)) -> BaseLLMProvider:
    """Get or create LLM provider instance."""
    global _llm_provider_instance

    if _llm_provider_instance is None:
        _llm_provider_instance = get_llm_provider(
            provider_type=settings.llm_provider,
            model_name=settings.llm_model_name,
            base_url=settings.llm_base_url,
            max_tokens=settings.llm_max_tokens,
            temperature=settings.llm_temperature
        )

    return _llm_provider_instance


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    settings: Settings = Depends(get_settings),
    llm_provider: BaseLLMProvider = Depends(get_llm_provider_instance)
) -> ChatResponse:
    """
    Process chat message and return response.

    Args:
        request: Chat request with user message
        settings: Application settings
        llm_provider: LLM provider instance

    Returns:
        Chat response with JARVIS reply

    Raises:
        HTTPException: If processing fails
    """
    try:
        user_message = request.message.strip()

        # Step 1: Classify intent (if enabled)
        if settings.enable_intent_classification:
            classifier = IntentClassifier(llm_provider)
            classification = classifier.classify(user_message)

            intent = classification["intent"]
            entities = classification.get("entities", {})
            confidence = classification.get("confidence", 0.0)

            # Check for errors in classification
            if "error" in classification:
                # Fallback: treat as general query
                intent = "general"
                entities = {}
                confidence = 0.0
        else:
            # Skip classification, treat as general query
            intent = "general"
            entities = {}
            confidence = 1.0

        # Step 2: Route to command handler (if enabled)
        if settings.enable_command_routing:
            router_service = CommandRouter(llm_provider)
            response_text = router_service.route(intent, entities, user_message)
        else:
            # Direct LLM response without routing
            llm_response = llm_provider.generate(
                prompt=user_message,
                system_prompt="You are JARVIS, a helpful assistant. Answer briefly.",
                max_tokens=settings.llm_max_tokens
            )

            if llm_response.error:
                raise HTTPException(status_code=500, detail=llm_response.error)

            response_text = llm_response.text.strip()

        # Step 3: Return response
        return ChatResponse(
            response=response_text,
            intent=str(intent),
            confidence=confidence,
            metadata={
                "entities": entities,
                "model": settings.llm_model_name or "default"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@router.get("/health")
async def health_check(
    llm_provider: BaseLLMProvider = Depends(get_llm_provider_instance)
) -> Dict[str, Any]:
    """
    Health check endpoint.

    Returns:
        Health status including LLM availability
    """
    llm_healthy = llm_provider.health_check()

    return {
        "status": "healthy" if llm_healthy else "degraded",
        "llm_available": llm_healthy,
        "service": "JARVIS Assistant"
    }
