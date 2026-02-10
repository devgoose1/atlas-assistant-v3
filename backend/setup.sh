#!/bin/bash
#
# JARVIS Assistant Setup Script
# Sets up Python virtual environment and installs dependencies

set -e

echo "🔧 Setting up JARVIS Assistant Backend..."

# Navigate to backend directory
cd "$(dirname "$0")"

# Check Python version
python3 --version

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✏️  Please edit .env to configure your LLM provider"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Edit .env to configure your LLM provider (Ollama or llama.cpp)"
echo "2. Start your LLM server:"
echo "   - Ollama: ollama run qwen:1.5b-chat-v1.5-q4_0"
echo "   - llama.cpp: ./server -m models/qwen-1_5b-chat-q4_0.gguf -c 2048 -ngl 0"
echo "3. Run './run.sh' to start JARVIS"
echo ""
