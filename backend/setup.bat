@echo off
REM JARVIS Assistant Setup Script for Windows
REM Sets up Python virtual environment and installs dependencies

echo Setting up JARVIS Assistant Backend...

cd /d "%~dp0"

REM Check Python version
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env to configure your LLM provider
    echo For development, leave LLM_PROVIDER=ollama
)

echo.
echo ============================================
echo Setup complete!
echo ============================================
echo.
echo Next steps:
echo 1. Install Ollama from https://ollama.ai
echo 2. Run: ollama run qwen:1.5b-chat-v1.5-q4_0
echo 3. Edit .env if needed (already configured for Ollama)
echo 4. Run: run.bat to start JARVIS
echo.
pause
