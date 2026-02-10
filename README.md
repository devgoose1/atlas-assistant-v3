# JARVIS - Local AI Assistant

A self-hosted AI assistant optimized for Raspberry Pi 4, featuring voice interaction through the browser and efficient local LLM inference.

## Features

- 🤖 **Local LLM**: Runs Qwen 1.5B Q4 (GGUF) via llama.cpp on Raspberry Pi 4
- 🎙️ **Voice Input**: Browser-based speech recognition (Web Speech API)
- 🔊 **Voice Output**: Text-to-speech responses
- 🧠 **Intent Classification**: Efficient intent detection optimized for small models
- ⚡ **Command Routing**: Smart routing between deterministic handlers and LLM
- 🌐 **Web UI**: Clean React interface accessible from any device on local network
- 🔄 **Dual LLM Support**: Switch between Ollama (dev) and llama.cpp (prod)
- 📦 **Minimal Dependencies**: Lightweight and resource-efficient

## Getting Started

Choose your setup guide based on your platform:

- 🪟 **[Windows Setup Guide](WINDOWS_SETUP.md)** - Complete guide for Windows development
- 🐧 **[Linux Setup Guide](LINUX_SETUP.md)** - Complete guide for Linux development
- 🥧 **[Raspberry Pi Deployment](DEPLOYMENT.md)** - Deploy to Raspberry Pi for production

**Quick Start Summary:**

1. Install prerequisites (Python, Node.js, Ollama)
2. Run backend setup script
3. Start Ollama and backend
4. Start frontend
5. Open browser to <http://localhost:5173/jarvis>

Detailed instructions for your platform are in the links above.

## Architecture

```text
┌──────────────────────────────────────┐
│          Browser (Any Device)        │
│  ┌────────────────────────────────┐  │
│  │  React Frontend                │  │
│  │  - Voice Input (Web Speech)    │  │
│  │  - Voice Output (TTS)          │  │
│  │  - Chat Interface              │  │
│  └────────────┬───────────────────┘  │
└───────────────┼──────────────────────┘
                │ HTTP REST API
                ▼
┌──────────────────────────────────────┐
│    Backend (Raspberry Pi 4)          │
│  ┌────────────────────────────────┐  │
│  │  FastAPI Server                │  │
│  │  - Intent Classifier           │  │
│  │  - Command Router              │  │
│  │  - LLM Provider Abstraction    │  │
│  └────────────┬───────────────────┘  │
│               ▼                      │
│  ┌────────────────────────────────┐  │
│  │  llama.cpp Server              │  │
│  │  Qwen 1.5B Q4 (GGUF)           │  │
│  │  CPU-only, 4 threads           │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

## System Requirements

### Production (Raspberry Pi 4)

- Raspberry Pi 4 (8GB RAM recommended, 4GB minimum)
- Raspbian OS / Raspberry Pi OS
- Python 3.9+
- llama.cpp compiled for ARM
- Qwen 1.5B Q4 GGUF model

### Development (Laptop/Desktop)

- Python 3.9+
- Node.js 18+
- Ollama (optional, for development)

## Quick Start

**For detailed platform-specific instructions, see:**

- 🪟 [Windows Setup Guide](WINDOWS_SETUP.md)
- 🐧 [Linux Setup Guide](LINUX_SETUP.md)
- 🥧 [Raspberry Pi Deployment](DEPLOYMENT.md)

**High-level Overview:**

### 1. Clone Repository

```bash
git clone <repository-url>
cd atlas-assistant-v3
```

### 2. Install Prerequisites

- Python 3.9+
- Node.js 18+
- Ollama (for development) OR llama.cpp (for production)

### 3. Setup and Start Backend

**Linux/Mac:**

```bash
cd backend
./setup.sh    # Setup
./run.sh      # Start
```

**Windows:**

```cmd
cd backend
setup.bat     # Setup
run.bat       # Start
```

### 4. Setup and Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### 5. Access JARVIS

Open browser: <http://localhost:5173/jarvis>

**See platform-specific guides above for detailed instructions and troubleshooting.**

## Project Structure

## Backend Setup

Backend runs on `http://0.0.0.0:8000`

## Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
```

Edit `.env` to set backend URL:

```env
VITE_API_URL=http://localhost:8000
```

For production (accessing from other devices):

```env
VITE_API_URL=http://raspberrypi.local:8000
```

### 6. Start Frontend

**Development:**

```bash
npm run dev
```

**Production:**

```bash
npm run build
npm start
```

### 7. Access JARVIS

Open your browser and navigate to:

- Development: `http://localhost:5173/jarvis`
- Production: `http://<raspberry-pi-ip>:3000/jarvis`

## Directory Structure

```text
atlas-assistant-v3/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── llm/                 # LLM abstraction layer
│   │   │   ├── base.py         # Base provider interface
│   │   │   ├── ollama_provider.py
│   │   │   └── llamacpp_provider.py
│   │   ├── routers/            # API routes
│   │   │   └── chat.py         # /api/chat endpoint
│   │   ├── services/           # Business logic
│   │   │   ├── intent_classifier.py
│   │   │   └── command_router.py
│   │   ├── config.py           # Configuration
│   │   └── main.py             # FastAPI app
│   ├── requirements.txt
│   ├── setup.sh
│   ├── run.sh
│   └── README.md
├── frontend/                     # React Frontend
│   ├── app/
│   │   ├── pages/
│   │   │   └── jarvis-chat/    # Chat interface
│   │   └── routes/
│   │       └── jarvis.tsx      # JARVIS route
│   ├── package.json
│   └── .env.example
└── README.md                     # This file
```

## API Documentation

### POST /api/chat

Send a message to JARVIS.

**Request:**

```json
{
  "message": "What time is it?"
}
```

**Response:**

```json
{
  "response": "It's currently 3:45 PM on Monday, February 10, 2026.",
  "intent": "time",
  "confidence": 1.0,
  "metadata": {
    "entities": {},
    "model": "qwen-1_5b-chat-q4_0.gguf"
  }
}
```

### GET /api/health

Check backend and LLM health.

**Response:**

```json
{
  "status": "healthy",
  "llm_available": true,
  "service": "JARVIS Assistant"
}
```

## Supported Intents

| Intent | Description | Example |
| -------- | ----------- | --------- |
| greeting | Greetings | "Hello", "Hi JARVIS" |
| time | Time queries | "What time is it?" |
| weather | Weather queries | "What's the weather?" (placeholder) |
| calculation | Math | "What's 25 * 4?" |
| timer | Set timers | "Set a timer for 5 minutes" (placeholder) |
| reminder | Set reminders | "Remind me to..." (placeholder) |
| question | General questions | "What is Python?" |
| general | Open conversation | Anything else |

## Voice Features

### Voice Input (🎤 button)

1. Click the microphone button
2. Speak your message
3. Click again to stop (or it stops automatically)
4. Message appears in input field

### Voice Response (🔊 Send & Speak button)

1. Type or speak your message
2. Click "Send & Speak" button
3. JARVIS responds with text and voice
4. Click "🔇 Stop" to interrupt

## Optimizations for Raspberry Pi

1. **Quantized Model**: Q4 quantization for 4x size reduction
2. **CPU-Only**: No GPU required
3. **4-Thread Inference**: Optimal for RPi4's 4 cores
4. **Small Token Limits**: 256 tokens max per response
5. **Low Temperature**: 0.1 for deterministic, less compute
6. **Pattern Matching**: Avoids LLM calls for simple queries
7. **Prompt Caching**: llama.cpp caches prompts to save CPU
8. **Short Context**: <1500 tokens to fit 2048 limit with headroom

## Configuration

### Backend (.env)

| Variable | Description | Default |
| ------------- | ----------- | --------- |
| `LLM_PROVIDER` | `ollama` or `llamacpp` | `ollama` |
| `LLM_BASE_URL` | LLM server URL | Provider-specific |
| `LLM_MODEL_NAME` | Model name | Provider-specific |
| `LLM_MAX_TOKENS` | Max tokens per response | `256` |
| `LLM_TEMPERATURE` | Sampling temperature | `0.1` |
| `HOST` | Server bind address | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `CORS_ORIGINS` | CORS allowed origins | `*` |

### Frontend (.env)

| Variable | Description | Default |
| ------------- | ----------- | --------- |
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |

## Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is available
lsof -i :8000

# Check backend health
curl http://localhost:8000/api/health
```

### LLM not responding

```bash
# Check if LLM server is running
# For Ollama:
curl http://localhost:11434/api/tags

# For llama.cpp:
curl http://localhost:8080/health
```

### High CPU usage on RPi

1. Verify using Q4 quantization (not Q8)
2. Set threads to 4 in llama.cpp: `-t 4`
3. Reduce `LLM_MAX_TOKENS` to 128
4. Increase temperature for faster sampling

### Voice features not working

- Voice features require HTTPS or localhost
- Check browser console for errors
- Verify browser supports Web Speech API (Chrome, Edge recommended)

## Extending JARVIS

### Adding New Intents

1. Add intent to `IntentType` enum in `backend/app/services/intent_classifier.py`
2. Add pattern matching (optional) in `_check_simple_patterns()`
3. Add handler in `backend/app/services/command_router.py`

### Integrating External APIs

Example: Weather API integration

```python
# backend/app/services/command_router.py

def _handle_weather(self, entities: Dict[str, Any]) -> str:
    import requests
    location = entities.get("location", "your location")

    # Call weather API
    response = requests.get(f"https://api.weather.com/...")
    data = response.json()

    return f"The weather in {location} is {data['condition']}..."
```

### Adding Persistent Memory

Consider adding:

- SQLite database for conversation history
- Redis for session state
- File-based storage for user preferences

## Performance Metrics

On Raspberry Pi 4 (8GB):

- **Response Time**: 2-5 seconds per message
- **Memory Usage**: ~1.5GB (model + runtime)
- **CPU Usage**: 80-100% during inference, 5% idle
- **Token Generation**: ~10-20 tokens/second

## Security Notes

- This is designed for **local network only**
- No authentication by default
- CORS set to `*` for local access
- Consider adding authentication for production use
- Do not expose to public internet without proper security

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please open an issue before submitting PRs.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [llama.cpp](https://github.com/ggerganov/llama.cpp)
- Model: [Qwen 1.5B](https://huggingface.co/Qwen)
- UI: [React Router](https://reactrouter.com/)

## Support

For issues and questions:

- Backend: See `backend/README.md`
- Check API health: `http://localhost:8000/api/health`
- View API docs: `http://localhost:8000/docs`
