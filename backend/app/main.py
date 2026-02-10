"""
JARVIS Assistant - Main Application

Local, self-hosted AI assistant optimized for Raspberry Pi 4.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import get_settings
from .routers import chat_router
from .routers.tools import router as tools_router


# Application lifespan for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    settings = get_settings()
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📡 LLM Provider: {settings.llm_provider}")
    print(f"🤖 Model: {settings.llm_model_name or 'default'}")
    print(f"🌐 Server: http://{settings.host}:{settings.port}")

    yield

    print("👋 Shutting down JARVIS Assistant")


# Create FastAPI app
app = FastAPI(
    title="JARVIS Assistant API",
    description="Local AI assistant optimized for Raspberry Pi 4",
    version="1.0.0",
    lifespan=lifespan
)


# Configure CORS for web UI access
settings = get_settings()
cors_origins = settings.cors_origins.split(",") if settings.cors_origins != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(chat_router)
app.include_router(tools_router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "JARVIS Assistant",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
