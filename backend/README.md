# JARVIS Assistant Backend

A local, self-hosted AI assistant backend optimized for Raspberry Pi 4 with Qwen 1.5B Q4 (GGUF).

## Features

- 🚀 **FastAPI Backend**: High-performance, async REST API
- 🤖 **LLM Abstraction**: Supports Ollama (dev) and llama.cpp (production)
- 🧠 **Intent Classification**: Efficient intent detection with small models
- 🎯 **Command Routing**: Smart routing to deterministic handlers
- 📦 **Minimal Dependencies**: Lightweight for Raspberry Pi
- 🔧 **Environment-based Config**: Easy switching between dev/prod
- 🌐 **CORS Enabled**: Access from any device on local network

## Architecture

```
┌─────────────┐
│   Web UI    │ (Browser with Web Speech API)
│  (Frontend) │
└──────┬──────┘
       │ HTTP POST /api/chat
       ▼
┌──────────────────────────────┐
│     FastAPI Backend          │
│  ┌────────────────────────┐  │
│  │  Intent Classifier     │  │
│  │  (Pattern + LLM)       │  │
│  └────────┬───────────────┘  │
│           ▼                  │
│  ┌────────────────────────┐  │
│  │  Command Router        │  │
│  │  (Deterministic +      │  │
│  │   LLM handlers)        │  │
│  └────────┬───────────────┘  │
│           ▼                  │
│  ┌────────────────────────┐  │
│  │  LLM Provider Layer    │  │
│  │  (Ollama / llama.cpp)  │  │
│  └────────┬───────────────┘  │
└───────────┼──────────────────┘
            ▼
    ┌───────────────┐
    │  Qwen 1.5B Q4 │
    │  (llama.cpp)  │
    └───────────────┘
```

## Requirements

- Python 3.9+
- Ollama (development) OR llama.cpp (production)
- Qwen 1.5B Q4 model

## Quick Start

### 1. Setup

```bash
cd backend
chmod +x setup.sh run.sh
./setup.sh
```

### 2. Configure

Edit `.env` to set your LLM provider:

**For development (Ollama):**
```env
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434
```

**For production (llama.cpp on Raspberry Pi):**
```env
LLM_PROVIDER=llamacpp
LLM_BASE_URL=http://localhost:8080
LLM_MODEL_NAME=qwen-1_5b-chat-q4_0.gguf
```

### 3. Start LLM Server

**Ollama (Development):**
```bash
ollama run qwen:1.5b-chat-v1.5-q4_0
```

**llama.cpp (Production on Raspberry Pi):**
```bash
cd /path/to/llama.cpp
./server -m models/qwen-1_5b-chat-q4_0.gguf \
         -c 2048 \
         -ngl 0 \
         --host 0.0.0.0 \
         --port 8080
```

### 4. Start JARVIS

```bash
./run.sh
```

The API will be available at `http://0.0.0.0:8000`

## API Endpoints

### POST /api/chat

Send a message to JARVIS.

**Request:**
```json
{
  "message": "Hello JARVIS"
}
```

**Response:**
```json
{
  "response": "Good evening! I'm JARVIS. How can I assist you?",
  "intent": "greeting",
  "confidence": 1.0,
  "metadata": {
    "entities": {},
    "model": "qwen-1_5b-chat-q4_0.gguf"
  }
}
```

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "llm_available": true,
  "service": "JARVIS Assistant"
}
```

## Supported Intents

- **greeting**: Greetings (Hello, Hi, etc.)
- **time**: Time queries (What time is it?)
- **weather**: Weather queries (placeholder)
- **calculation**: Math calculations
- **timer**: Timer requests (placeholder)
- **reminder**: Reminder requests (placeholder)
- **question**: General questions
- **general**: General conversation

## Configuration

All configuration is done via environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM backend: `ollama` or `llamacpp` | `ollama` |
| `LLM_BASE_URL` | LLM server URL | Provider-specific |
| `LLM_MODEL_NAME` | Model name | Provider-specific |
| `LLM_MAX_TOKENS` | Max tokens per response | `256` |
| `LLM_TEMPERATURE` | Sampling temperature | `0.1` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `CORS_ORIGINS` | Allowed origins | `*` |

## Project Structure

```
backend/
├── app/
│   ├── llm/                    # LLM abstraction layer
│   │   ├── base.py            # Base provider interface
│   │   ├── ollama_provider.py # Ollama implementation
│   │   ├── llamacpp_provider.py # llama.cpp implementation
│   │   └── __init__.py
│   ├── routers/               # API routes
│   │   ├── chat.py           # Chat endpoint
│   │   └── __init__.py
│   ├── services/              # Business logic
│   │   ├── intent_classifier.py # Intent classification
│   │   ├── command_router.py    # Command routing
│   │   └── __init__.py
│   ├── config.py              # Configuration management
│   └── main.py                # FastAPI application
├── requirements.txt           # Python dependencies
├── .env.example              # Example configuration
├── setup.sh                  # Setup script
└── run.sh                    # Run script
```

## Optimizations for Raspberry Pi

1. **Low temperature (0.1)**: More deterministic, less compute
2. **Small token limits (256)**: Faster inference
3. **Pattern matching**: Avoid LLM calls for simple queries
4. **Minimal context (<1500 tokens)**: Fit within 2048 limit with headroom
5. **Cache prompts**: llama.cpp caches prompts to save CPU
6. **4-thread inference**: Optimal for RPi4's 4 cores

## Development

### Running in Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

FastAPI provides automatic interactive documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### LLM Provider Not Available

Check health endpoint:
```bash
curl http://localhost:8000/api/health
```

If `llm_available: false`:
1. Verify LLM server is running
2. Check `LLM_BASE_URL` in `.env`
3. Test LLM server directly:
   - Ollama: `curl http://localhost:11434/api/tags`
   - llama.cpp: `curl http://localhost:8080/health`

### High Memory Usage on Raspberry Pi

1. Use Q4 quantized model (not Q8 or higher)
2. Reduce `LLM_MAX_TOKENS`
3. Set `MAX_CONTEXT_LENGTH` to 1500 or lower
4. Close other applications

### Slow Response Times

1. Use pattern matching (already enabled for greetings, time, weather)
2. Reduce `LLM_MAX_TOKENS`
3. Lower temperature (already at 0.1)
4. Consider using Q3 quantization (less accurate but faster)

## License

MIT License - see LICENSE file for details

## Contributing

This is a personal project, but contributions are welcome! Please open an issue before submitting PRs.
