@echo off
REM Meeting Intelligence Assistant - Windows Startup Script

setlocal enabledelayedexpansion

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3.12+ is required but not found in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo Warning: .env file not found. Copying from .env.example
    if exist ".env.example" (
        copy .env.example .env
        echo Created .env file. Please edit it with your API keys.
    ) else (
        echo Error: .env.example not found
        pause
        exit /b 1
    )
)

REM Create necessary directories
if not exist "data\uploads" mkdir data\uploads
if not exist "data\temp" mkdir data\temp
if not exist "data\models" mkdir data\models
if not exist "data\exports" mkdir data\exports
if not exist "logs" mkdir logs

echo.
echo ===============================================
echo  Meeting Intelligence Assistant
echo  Startup Script for Windows
echo ===============================================
echo.

REM Check for required packages
echo Checking Python dependencies...
python -c "import fastapi, streamlit, sqlalchemy, pydantic" >nul 2>&1
if errorlevel 1 (
    echo Missing dependencies. Running: pip install -r requirements.txt
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies OK
echo.

REM Start the application
echo Starting Meeting Intelligence Assistant...
echo.
echo Backend URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend URL: http://localhost:8501
echo.

REM Check for FFmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo Warning: FFmpeg not found. Video processing will not work.
    echo Install FFmpeg: choco install ffmpeg
    echo Or download from: https://ffmpeg.org/download.html
    echo.
)

REM Start in separate windows
echo Starting FastAPI backend...
start "Meeting Intelligence - API Backend" cmd /k python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

timeout /t 3 /nobreak

echo.
echo Starting Streamlit frontend...
start "Meeting Intelligence - UI Frontend" cmd /k streamlit run app\ui\streamlit_app.py --logger.level=info

echo.
echo Startup complete. Check the command windows for logs.
echo If browser doesn't open automatically, visit: http://localhost:8501
echo.
pause
