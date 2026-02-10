# JARVIS Quick Reference

Quick commands for common operations.

## Development

### Start Everything (Development)

```bash
# Terminal 1: Start Ollama
ollama run qwen:1.5b-chat-v1.5-q4_0

# Terminal 2: Start Backend
cd backend
./run.sh

# Terminal 3: Start Frontend
cd frontend
npm run dev
```

Access: http://localhost:5173/jarvis

## Production (Raspberry Pi)

### Service Management

```bash
# Start services
sudo systemctl start llamacpp-server.service
sudo systemctl start jarvis-backend.service
sudo systemctl start jarvis-frontend.service

# Stop services
sudo systemctl stop llamacpp-server.service
sudo systemctl stop jarvis-backend.service
sudo systemctl stop jarvis-frontend.service

# Restart services
sudo systemctl restart llamacpp-server.service
sudo systemctl restart jarvis-backend.service
sudo systemctl restart jarvis-frontend.service

# Check status
sudo systemctl status llamacpp-server.service
sudo systemctl status jarvis-backend.service
sudo systemctl status jarvis-frontend.service

# View logs
sudo journalctl -u jarvis-backend.service -f
sudo journalctl -u llamacpp-server.service -f
```

### Health Checks

```bash
# Check llama.cpp
curl http://localhost:8080/health

# Check backend
curl http://localhost:8000/api/health

# Test chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root info |
| `/docs` | GET | API documentation |
| `/api/chat` | POST | Send message |
| `/api/health` | GET | Health check |

## Environment Variables

### Backend (.env)

```env
# LLM Provider - "ollama" or "llamacpp"
LLM_PROVIDER=llamacpp

# LLM Server URL
LLM_BASE_URL=http://localhost:8080

# Server Settings
HOST=0.0.0.0
PORT=8000

# Performance
LLM_MAX_TOKENS=256
LLM_TEMPERATURE=0.1
```

### Frontend (.env)

```env
# Backend API URL
VITE_API_URL=http://localhost:8000
```

## File Locations

### Backend
- Main app: `backend/app/main.py`
- Config: `backend/app/config.py`
- Intent classifier: `backend/app/services/intent_classifier.py`
- Command router: `backend/app/services/command_router.py`
- LLM providers: `backend/app/llm/`

### Frontend
- Chat UI: `frontend/app/pages/jarvis-chat/jarvis-chat.tsx`
- Routes: `frontend/app/routes/jarvis.tsx`

## Common Tasks

### Add New Intent

1. Edit `backend/app/services/intent_classifier.py`:
```python
class IntentType(str, Enum):
    # ... existing intents
    MY_NEW_INTENT = "my_new_intent"
```

2. Add handler in `backend/app/services/command_router.py`:
```python
def route(self, intent, entities, user_input):
    # ...
    elif intent_type == IntentType.MY_NEW_INTENT:
        return self._handle_my_new_intent(entities)

def _handle_my_new_intent(self, entities):
    return "Response for my new intent"
```

3. Restart backend

### Change LLM Provider

Edit `backend/.env`:
```env
# Switch to Ollama
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434

# OR switch to llama.cpp
LLM_PROVIDER=llamacpp
LLM_BASE_URL=http://localhost:8080
```

Restart backend.

### Update Dependencies

Backend:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

Frontend:
```bash
cd frontend
npm install
```

### View Logs

```bash
# Backend logs (systemd)
sudo journalctl -u jarvis-backend.service -f

# Backend logs (manual run)
cd backend && ./run.sh

# Frontend logs
cd frontend && npm run dev
```

### Test API

```bash
# Health check
curl http://localhost:8000/api/health

# Send message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What time is it?"}'

# Pretty print with jq
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}' | jq
```

## Performance Tuning

### Low Memory Situation
```env
LLM_MAX_TOKENS=128
MAX_CONTEXT_LENGTH=1024
```

### High CPU Usage
```env
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=128
```

### Slow Response
- Use pattern matching for common queries
- Reduce context length
- Use Q3 quantization instead of Q4

## Troubleshooting

### "Connection refused"
- Check if service is running: `sudo systemctl status jarvis-backend.service`
- Check if port is in use: `lsof -i :8000`

### "LLM not available"
- Check LLM server: `curl http://localhost:8080/health`
- Check LLM_BASE_URL in .env
- View logs: `sudo journalctl -u llamacpp-server.service -f`

### "Out of memory"
- Use Q4 quantization
- Reduce MAX_TOKENS
- Add swap space
- Close other applications

### Voice not working
- Use HTTPS or localhost
- Check browser console
- Verify Web Speech API support (Chrome/Edge)

## URLs

### Development
- Frontend: http://localhost:5173/jarvis
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Production
- Frontend: http://raspberrypi.local:3000/jarvis
- Backend: http://raspberrypi.local:8000
- API Docs: http://raspberrypi.local:8000/docs

## System Info

```bash
# Check Python version
python3 --version

# Check Node version
node --version

# Check disk space
df -h

# Check memory
free -h

# Check CPU temperature (RPi)
vcgencmd measure_temp

# Check running services
systemctl list-units --state=running | grep jarvis
```

## Useful Links

- Backend README: `backend/README.md`
- Deployment Guide: `DEPLOYMENT.md`
- Main README: `README.md`
- API Docs: http://localhost:8000/docs
