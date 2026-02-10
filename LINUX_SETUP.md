# JARVIS Local Development Guide (Linux)

Quick guide to get JARVIS running on your Linux development machine.

## Prerequisites

1. **Python 3.9+** (usually pre-installed on most Linux distributions)
2. **Node.js 18+**
3. **Ollama** (for local LLM)
4. **Git** (usually pre-installed)

## Quick Install Prerequisites

### Ubuntu/Debian/Pop!_OS/Linux Mint

```bash
# Update package list
sudo apt update

# Install Python and development tools (if not already installed)
sudo apt install -y python3 python3-pip python3-venv

# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

### Fedora/RHEL/CentOS

```bash
# Install Python and development tools
sudo dnf install -y python3 python3-pip

# Install Node.js 18.x
sudo dnf install -y nodejs

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

### Arch Linux/Manjaro

```bash
# Install Python and Node.js
sudo pacman -S python python-pip nodejs npm

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

## Step-by-Step Setup

### 1. Setup Backend

Open a terminal:

```bash
cd backend
chmod +x setup.sh run.sh
./setup.sh
```

This will:

- Create a Python virtual environment
- Install all dependencies
- Create a `.env` file with defaults

### 2. Start Ollama

Open a **new terminal** and run:

```bash
ollama run qwen:1.5b-chat-v1.5-q4_0
```

This will:

- Download the Qwen 1.5B model (first time only, ~900MB)
- Start the Ollama server on port 11434
- Keep it running in this terminal

**Leave this terminal open!**

### 3. Start Backend

Open a **new terminal** and run:

```bash
cd backend
./run.sh
```

The backend will be available at: <http://localhost:8000>

**Leave this terminal open!**

### 4. Setup Frontend

Open a **new terminal** and run:

```bash
cd frontend
npm install
cp .env.example .env
```

Edit `frontend/.env` if needed:

```bash
nano .env
# or
vim .env
# or
gedit .env
```

Content should be:

```env
VITE_API_URL=http://localhost:8000
```

### 5. Start Frontend

In the same terminal:

```bash
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
   🤖 Model: default
   🌐 Server: http://0.0.0.0:8000
   ```

3. **Terminal 3**: Frontend dev server

   ```text
   VITE v5.x.x ready in 500ms
   ➜ Local: http://localhost:5173/
   ➜ Network: use --host to expose
   ```

## Testing JARVIS

### Test 1: Health Check

Open a new terminal:

```bash
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

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello JARVIS"}'
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

### "python3: command not found"

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

### "node: command not found"

```bash
# Install using NodeSource (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Or use nvm (all distros)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
```

### "ollama: command not found"

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

### Backend shows "LLM not available"

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama run qwen:1.5b-chat-v1.5-q4_0

# Check backend .env file
cat backend/.env | grep LLM_BASE_URL
# Should be: LLM_BASE_URL=http://localhost:11434 (or not set)
```

### "Connection refused" in frontend

```bash
# Make sure backend is running
curl http://localhost:8000/api/health

# Check frontend .env
cat frontend/.env
# Should have: VITE_API_URL=http://localhost:8000

# Restart frontend after changing .env
cd frontend
npm run dev
```

### Voice features not working

- Voice requires Chrome, Edge, or Safari (not Firefox)
- Check browser console for errors (F12)
- Microphone permission must be granted
- On Linux, check audio permissions:

  ```bash
  # Check if user is in audio group
  groups $USER

  # Add user to audio group if needed
  sudo usermod -a -G audio $USER
  # Log out and back in
  ```

### Port already in use

```bash
# Check what's using port 8000
sudo lsof -i :8000
# or
sudo netstat -tulpn | grep 8000

# Kill the process or change port in backend/.env
echo "PORT=8001" >> backend/.env
```

To change frontend port, edit `vite.config.ts`:

```typescript
server: {
  port: 5174
}
```

### Permission denied on scripts

```bash
chmod +x backend/setup.sh backend/run.sh
```

## Quick Commands Reference

### Start Everything

```bash
# Terminal 1
ollama run qwen:1.5b-chat-v1.5-q4_0

# Terminal 2
cd backend && ./run.sh

# Terminal 3
cd frontend && npm run dev
```

### Stop Everything

Press `Ctrl+C` in each terminal.

### Restart Backend Only

In Terminal 2, press `Ctrl+C`, then:

```bash
./run.sh
```

### Check Status

```bash
# Check backend
curl http://localhost:8000/api/health

# Check Ollama
curl http://localhost:11434/api/tags

# Check what's running on ports
sudo lsof -i :8000,11434,5173
```

### View Running Processes

```bash
# Check Ollama
ps aux | grep ollama

# Check Python backend
ps aux | grep uvicorn

# Check Node frontend
ps aux | grep vite
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

Backend logs appear in Terminal 2. For more details, add to `backend/.env`:

```bash
echo "DEBUG=true" >> backend/.env
```

### Test Without Frontend

Use the interactive API docs:

1. Go to <http://localhost:8000/docs>
2. Click "POST /api/chat"
3. Click "Try it out"
4. Enter a message and click "Execute"

### Using Different Models

To use a different Ollama model:

```bash
# List available models
ollama list

# Pull a different model
ollama pull llama2:7b

# Update backend/.env
echo "LLM_MODEL_NAME=llama2:7b" >> backend/.env
```

Restart backend after changing models.

### Run in Background (tmux)

For a cleaner workflow, use tmux:

```bash
# Install tmux
sudo apt install tmux  # Ubuntu/Debian
sudo dnf install tmux  # Fedora
sudo pacman -S tmux    # Arch

# Start tmux session
tmux new -s jarvis

# Create windows (Ctrl+B then C)
# Window 1: ollama run qwen:1.5b-chat-v1.5-q4_0
# Switch to new window (Ctrl+B then C)
# Window 2: cd backend && ./run.sh
# Switch to new window (Ctrl+B then C)
# Window 3: cd frontend && npm run dev

# Detach from session: Ctrl+B then D
# Reattach later: tmux attach -t jarvis
# List windows: Ctrl+B then W
```

### Run in Background (screen)

Alternative to tmux:

```bash
# Start Ollama in background
screen -dmS ollama ollama run qwen:1.5b-chat-v1.5-q4_0

# Start backend in background
cd backend
screen -dmS backend ./run.sh

# Start frontend in background
cd frontend
screen -dmS frontend npm run dev

# List sessions
screen -ls

# Attach to a session
screen -r ollama

# Detach: Ctrl+A then D
```

## Performance Notes

On development machines:

- Response time: < 1 second (depending on CPU)
- Memory usage: ~2GB (Ollama + model)
- Token generation: 50-100 tokens/second

On laptop with less RAM:

- Consider using a smaller model: `qwen:0.5b`
- Or use Ollama with CPU-only mode (default on Linux)

On Raspberry Pi 4 (production):

- Response time: 2-5 seconds
- Memory usage: ~1.5GB
- Token generation: 10-20 tokens/second

## System Resource Monitoring

```bash
# Check CPU and memory usage
htop
# or
top

# Check GPU usage (if using GPU)
nvidia-smi

# Watch memory usage
watch -n 1 free -h

# Check disk space
df -h

# Monitor network
sudo nethogs
```

## Firewall Configuration

If you have a firewall enabled:

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 8000/tcp   # Backend
sudo ufw allow 11434/tcp  # Ollama
sudo ufw allow 5173/tcp   # Frontend

# firewalld (Fedora/RHEL)
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --permanent --add-port=11434/tcp
sudo firewall-cmd --permanent --add-port=5173/tcp
sudo firewall-cmd --reload

# iptables (manual)
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 11434 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5173 -j ACCEPT
```

## Running as Systemd Services (Optional)

For development, you can set up systemd services:

```bash
# Create user service directory
mkdir -p ~/.config/systemd/user

# Create Ollama service
cat > ~/.config/systemd/user/jarvis-ollama.service << 'EOF'
[Unit]
Description=Ollama for JARVIS Development

[Service]
Type=simple
ExecStart=/usr/bin/ollama run qwen:1.5b-chat-v1.5-q4_0
Restart=on-failure

[Install]
WantedBy=default.target
EOF

# Enable and start
systemctl --user enable jarvis-ollama.service
systemctl --user start jarvis-ollama.service

# Check status
systemctl --user status jarvis-ollama.service
```

## Accessing from Other Devices on Network

To access JARVIS from your phone or tablet on the same network:

1. Find your machine's IP:

   ```bash
   hostname -I
   # or
   ip addr show | grep "inet "
   ```

2. Edit `frontend/.env`:

   ```env
   VITE_API_URL=http://192.168.1.X:8000
   ```

   Replace `192.168.1.X` with your machine's IP

3. Start frontend with host flag:

   ```bash
   npm run dev -- --host
   ```

4. Access from other device:

   ```text
   http://192.168.1.X:5173/jarvis
   ```

## Support

- Backend issues: Check `backend/README.md`
- API documentation: <http://localhost:8000/docs>
- Deployment guide: `DEPLOYMENT.md`
- Quick reference: `QUICKREF.md`
- Linux-specific issues: Check your distro's wiki or forums
