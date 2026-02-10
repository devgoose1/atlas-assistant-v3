# JARVIS Raspberry Pi Deployment Guide

Complete guide for deploying JARVIS on your Raspberry Pi 4.

## Prerequisites

- Raspberry Pi 4 (8GB RAM recommended, 4GB minimum)
- Raspberry Pi OS (64-bit recommended)
- At least 8GB free storage
- Stable internet connection for initial setup

## Step 1: System Update

```bash
sudo apt update
sudo apt upgrade -y
```

## Step 2: Install Dependencies

```bash
# Install Python 3 and development tools
sudo apt install -y python3 python3-pip python3-venv git build-essential

# Install Node.js (for frontend)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

## Step 3: Clone Repository

```bash
cd ~
git clone <your-repo-url> atlas-assistant-v3
cd atlas-assistant-v3
```

## Step 4: Setup llama.cpp

```bash
# Clone and build llama.cpp
cd ~
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

# Create models directory
mkdir -p models
cd models
```

Download Qwen 1.5B Q4 model:
```bash
# Option 1: Direct download (if available)
wget https://huggingface.co/Qwen/Qwen-1_5B-Chat-GGUF/resolve/main/qwen-1_5b-chat-q4_0.gguf

# Option 2: Use huggingface-cli
pip3 install huggingface-hub
huggingface-cli download Qwen/Qwen-1_5B-Chat-GGUF qwen-1_5b-chat-q4_0.gguf --local-dir .
```

Test llama.cpp:
```bash
cd ~/llama.cpp
./server -m models/qwen-1_5b-chat-q4_0.gguf -c 2048 -ngl 0 -t 4
# Press Ctrl+C to stop after verifying it starts
```

## Step 5: Setup Backend

```bash
cd ~/atlas-assistant-v3/backend
chmod +x setup.sh run.sh
./setup.sh
```

Configure for production:
```bash
nano .env
```

Set these values:
```env
LLM_PROVIDER=llamacpp
LLM_BASE_URL=http://localhost:8080
LLM_MODEL_NAME=qwen-1_5b-chat-q4_0.gguf
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

Test backend:
```bash
./run.sh
# Press Ctrl+C after verifying it starts
```

## Step 6: Setup Frontend

```bash
cd ~/atlas-assistant-v3/frontend
npm install
cp .env.example .env
```

Configure frontend:
```bash
nano .env
```

Set backend URL (use your Pi's IP or hostname):
```env
VITE_API_URL=http://raspberrypi.local:8000
```

Build frontend:
```bash
npm run build
```

## Step 7: Setup Auto-Start Services

### Setup llama.cpp service

```bash
# Copy service file
sudo cp ~/atlas-assistant-v3/backend/llamacpp-server.service /etc/systemd/system/

# Edit paths if needed
sudo nano /etc/systemd/system/llamacpp-server.service

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable llamacpp-server.service
sudo systemctl start llamacpp-server.service

# Check status
sudo systemctl status llamacpp-server.service
```

### Setup JARVIS backend service

```bash
# Copy service file
sudo cp ~/atlas-assistant-v3/backend/jarvis-backend.service /etc/systemd/system/

# Edit paths if needed
sudo nano /etc/systemd/system/jarvis-backend.service

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable jarvis-backend.service
sudo systemctl start jarvis-backend.service

# Check status
sudo systemctl status jarvis-backend.service
```

### Setup frontend service (optional - for production)

Create frontend service:
```bash
sudo nano /etc/systemd/system/jarvis-frontend.service
```

Contents:
```ini
[Unit]
Description=JARVIS Frontend Service
After=network.target jarvis-backend.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/atlas-assistant-v3/frontend
Environment="PATH=/usr/bin"
ExecStart=/usr/bin/npm start
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable jarvis-frontend.service
sudo systemctl start jarvis-frontend.service
sudo systemctl status jarvis-frontend.service
```

## Step 8: Verify Installation

### Check all services
```bash
sudo systemctl status llamacpp-server.service
sudo systemctl status jarvis-backend.service
sudo systemctl status jarvis-frontend.service
```

### Test endpoints
```bash
# Test llama.cpp
curl http://localhost:8080/health

# Test backend
curl http://localhost:8000/api/health

# Test chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello JARVIS"}'
```

### Access from browser

From any device on your local network:
```
http://raspberrypi.local:3000/jarvis
```

Or using IP address:
```
http://192.168.1.X:3000/jarvis
```

## Step 9: Configure Firewall (Optional)

If using firewall:
```bash
sudo ufw allow 8000/tcp  # Backend
sudo ufw allow 8080/tcp  # llama.cpp
sudo ufw allow 3000/tcp  # Frontend
sudo ufw enable
```

## Troubleshooting

### Services won't start

Check logs:
```bash
# llama.cpp logs
sudo journalctl -u llamacpp-server.service -f

# Backend logs
sudo journalctl -u jarvis-backend.service -f

# Frontend logs
sudo journalctl -u jarvis-frontend.service -f
```

### High CPU usage

This is normal during LLM inference. To reduce:
1. Lower `LLM_MAX_TOKENS` to 128 in backend/.env
2. Increase temperature to 0.3
3. Close other applications

### Out of memory

1. Use Q4 quantization (not Q8)
2. Reduce context length: `LLM_MAX_CONTEXT=1024`
3. Add swap space:
```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Can't access from other devices

1. Check firewall settings
2. Verify Pi's IP: `hostname -I`
3. Test connectivity: `ping raspberrypi.local`
4. Check CORS settings in backend/.env

### llama.cpp crashes

1. Reduce threads: change `-t 4` to `-t 2`
2. Reduce context: change `-c 2048` to `-c 1024`
3. Check model file integrity
4. Monitor memory: `free -h`

## Maintenance

### View logs
```bash
# View llama.cpp logs
sudo journalctl -u llamacpp-server.service --since today

# View backend logs
sudo journalctl -u jarvis-backend.service --since today

# View frontend logs
sudo journalctl -u jarvis-frontend.service --since today
```

### Restart services
```bash
sudo systemctl restart llamacpp-server.service
sudo systemctl restart jarvis-backend.service
sudo systemctl restart jarvis-frontend.service
```

### Update JARVIS
```bash
cd ~/atlas-assistant-v3
git pull

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart jarvis-backend.service

# Update frontend
cd ../frontend
npm install
npm run build
sudo systemctl restart jarvis-frontend.service
```

### Monitor performance
```bash
# CPU and memory
htop

# Temperature
vcgencmd measure_temp

# Service status
systemctl list-units --state=running | grep jarvis
```

## Performance Tips

1. **Overclock (optional)**: Edit `/boot/config.txt` to add:
   ```
   over_voltage=2
   arm_freq=1750
   ```
   ⚠️ Warning: Requires adequate cooling

2. **Disable desktop environment**: If running headless:
   ```bash
   sudo systemctl set-default multi-user.target
   ```

3. **Close unnecessary services**:
   ```bash
   sudo systemctl disable bluetooth
   sudo systemctl disable cups
   ```

4. **Add cooling**: Use a fan or heatsink for sustained performance

## Security Recommendations

1. **Change default password**:
   ```bash
   passwd
   ```

2. **Setup SSH keys** (instead of password):
   ```bash
   ssh-keygen -t ed25519
   # Copy public key to other devices
   ```

3. **Disable SSH password authentication**:
   ```bash
   sudo nano /etc/ssh/sshd_config
   # Set: PasswordAuthentication no
   sudo systemctl restart ssh
   ```

4. **Keep system updated**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

5. **Don't expose to public internet** without proper authentication

## Backup

Create a backup script:
```bash
nano ~/backup-jarvis.sh
```

Contents:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf ~/jarvis-backup-$DATE.tar.gz \
    ~/atlas-assistant-v3/backend/.env \
    ~/atlas-assistant-v3/frontend/.env
echo "Backup created: jarvis-backup-$DATE.tar.gz"
```

Make executable and run:
```bash
chmod +x ~/backup-jarvis.sh
./backup-jarvis.sh
```

## Next Steps

1. Customize intents in `backend/app/services/intent_classifier.py`
2. Add new commands in `backend/app/services/command_router.py`
3. Integrate external APIs (weather, calendar, etc.)
4. Add persistent storage for conversation history
5. Customize frontend UI in `frontend/app/pages/jarvis-chat/`

## Support

- Check logs: `sudo journalctl -u jarvis-backend.service -f`
- API docs: `http://raspberrypi.local:8000/docs`
- Health check: `http://raspberrypi.local:8000/api/health`
