@echo off
REM JARVIS Assistant Startup Script for Windows
REM Starts the FastAPI backend server

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo ERROR: Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo WARNING: No .env file found. Using defaults.
    echo TIP: Copy .env.example to .env and customize settings.
    echo.
)

REM Start the server
echo Starting JARVIS Assistant...
echo Backend will be available at http://localhost:8000
echo Press Ctrl+C to stop
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
