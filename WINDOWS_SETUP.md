# JARVIS Local Development Guide (Windows)

Quick guide to get JARVIS running on your Windows development machine.

## Prerequisites

1. **Python 3.9+**: Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Node.js 18+**: Download from [nodejs.org](https://nodejs.org/)

3. **Ollama**: Download from [ollama.ai](https://ollama.ai/download)

## Step-by-Step Setup

### 1. Setup Backend

Open PowerShell or Command Prompt:

```cmd
cd backend
setup.bat
```

This will:

- Create a Python virtual environment
- Install all dependencies
- Create a `.env` file with defaults

### 2. Start Ollama

Open a **new terminal** and run:

```cmd
ollama run qwen:1.5b-chat-v1.5-q4_0
```

This will:

- Download the Qwen 1.5B model (first time only, ~900MB)
- Start the Ollama server on port 11434
- Keep it running in this terminal

**Leave this terminal open!**

### 3. Start Backend

Open a **new terminal** and run:

```cmd
cd backend
run.bat
```

The backend will be available at: <http://localhost:8000>

**Leave this terminal open!**

### 4. Setup Frontend

Open a **new terminal** and run:

```cmd
cd frontend
npm install
copy .env.example .env
```

Edit `frontend\.env` if needed:

```env
VITE_API_URL=http://localhost:8000
```

### 5. Start Frontend

In the same terminal:

```cmd
npm run dev
```

The frontend will be available at: <http://localhost:5173>

**Leave this terminal open!**

### 6. Access JARVIS

Open your browser and go to:

```text
http://localhost:5173/jarvis
```

## What You Should See

You should now have 3 terminals running:

1. **Terminal 1**: Ollama server

   ```text
   >>> qwen:1.5b-chat-v1.5-q4_0 ready
   ```

2. **Terminal 2**: JARVIS Backend

   ```text
   🚀 Starting JARVIS Assistant v1.0.0
   📡 LLM Provider: ollama
   🌐 Server: http://0.0.0.0:8000
   ```

3. **Terminal 3**: Frontend dev server

   ```text
   VITE ready in 500ms
   ➜ Local: http://localhost:5173/
   ```

## Testing JARVIS

### Test 1: Health Check

Open a new terminal:

```cmd
curl http://localhost:8000/api/health
```

Should return:

```json
{
  "status": "healthy",
  "llm_available": true,
  "service": "JARVIS Assistant"
}
```

### Test 2: Chat via API

```cmd
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"message\": \"Hello JARVIS\"}"
```

### Test 3: Web UI

1. Go to <http://localhost:5173/jarvis>
2. Type "Hello" and click Send
3. JARVIS should respond with a greeting

### Test 4: Voice Input (in browser)

1. Click the 🎤 microphone button
2. Say "What time is it?"
3. Click 🎤 again to stop
4. Your speech should appear in the input field
5. Click "Send" or "🔊 Send & Speak"

## Troubleshooting

### "Python not found"

- Install Python from python.org
- Make sure "Add Python to PATH" was checked during installation
- Restart your terminal after installation

### "npm not found"

- Install Node.js from nodejs.org
- Restart your terminal after installation

### "ollama not found"

- Install Ollama from ollama.ai
- Restart your terminal after installation

### Backend shows "LLM not available"

- Make sure Ollama is running: `ollama run qwen:1.5b-chat-v1.5-q4_0`
- Check that Ollama is on port 11434: <http://localhost:11434>
- Verify `LLM_BASE_URL=http://localhost:11434` in `backend\.env`

### "Connection refused" in frontend

- Make sure backend is running on port 8000
- Check `VITE_API_URL=http://localhost:8000` in `frontend\.env`
- Restart frontend after changing .env: `npm run dev`

### Voice features not working

- Voice requires Chrome, Edge, or Safari (not Firefox)
- Check browser console for errors (F12)
- Microphone permission must be granted

### Port already in use

If port 8000 or 5173 is already in use:

**Backend** - edit `backend\.env`:

```env
PORT=8001
```

**Frontend** - edit `vite.config.ts`:

```typescript
server: {
  port: 5174
}
```

## Quick Commands Reference

### Start Everything

```cmd
REM Terminal 1
ollama run qwen:1.5b-chat-v1.5-q4_0

REM Terminal 2
cd backend && run.bat

REM Terminal 3
cd frontend && npm run dev
```

### Stop Everything

Press `Ctrl+C` in each terminal.

### Restart Backend Only

In Terminal 2, press `Ctrl+C`, then:

```cmd
run.bat
```

### Check Status

```cmd
REM Check backend
curl http://localhost:8000/api/health

REM Check Ollama
curl http://localhost:11434/api/tags
```

## Next Steps

Once everything works locally:

1. ✅ Test all voice features
2. ✅ Try different queries (time, greetings, questions)
3. ✅ Verify response times are acceptable
4. ✅ Check the API docs: <http://localhost:8000/docs>
5. 🚀 Ready to deploy to Raspberry Pi? See `DEPLOYMENT.md`

## Development Tips

### Auto-reload

Both backend and frontend have auto-reload enabled:

- Backend: Edit any `.py` file → server restarts automatically
- Frontend: Edit any `.tsx` file → browser updates automatically

### View Logs

Backend logs appear in Terminal 2. For more details, add to `backend\.env`:

```env
DEBUG=true
```

### Test Without Frontend

Use the interactive API docs:

1. Go to <http://localhost:8000/docs>
2. Click "POST /api/chat"
3. Click "Try it out"
4. Enter a message and click "Execute"

### Using Different Models

To use a different Ollama model:

```cmd
REM List available models
ollama list

REM Pull a different model
ollama pull llama2:7b

REM Update backend\.env
LLM_MODEL_NAME=llama2:7b
```

Restart backend after changing models.

## Performance Notes

On development machines:

- Response time: < 1 second (depending on CPU)
- Memory usage: ~2GB (Ollama + model)
- Token generation: 50-100 tokens/second

On Raspberry Pi 4 (production):

- Response time: 2-5 seconds
- Memory usage: ~1.5GB
- Token generation: 10-20 tokens/second

## Support

- Backend issues: Check `backend/README.md`
- API documentation: <http://localhost:8000/docs>
- Deployment guide: `DEPLOYMENT.md`
- Quick reference: `QUICKREF.md`
