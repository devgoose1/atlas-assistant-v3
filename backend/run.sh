#!/bin/bash
#
# JARVIS Assistant Startup Script
# Starts the FastAPI backend server

set -e

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Using defaults."
    echo "💡 Tip: Copy .env.example to .env and customize settings."
fi

# Start the server
echo "🚀 Starting JARVIS Assistant..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
