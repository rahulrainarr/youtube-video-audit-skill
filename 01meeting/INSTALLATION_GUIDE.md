# Installation Guide

## Prerequisites

- Windows 11 (Windows 10 may work)
- Python 3.12+
- pip (comes with Python)
- FFmpeg (for video processing)

## Step 1: Install Python 3.12+

### Option A: Using Windows installer
1. Download from https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Choose "Install Now"

**Verify:**
```powershell
python --version
# Should show: Python 3.12.x
```

### Option B: Using Windows Package Manager (winget)
```powershell
winget install Python.Python.3.12
```

### Option C: Using Chocolatey
```powershell
choco install python
```

## Step 2: Install FFmpeg

### Option A: Using Chocolatey (Recommended)
```powershell
# Run as Administrator
choco install ffmpeg
```

### Option B: Using Windows Package Manager
```powershell
winget install FFmpeg
```

### Option C: Manual Installation
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\Program Files\FFmpeg`
3. Add `C:\Program Files\FFmpeg\bin` to Windows PATH
   - Right-click "This PC" → Properties → Environment Variables
   - Edit PATH and add the FFmpeg bin directory

**Verify:**
```powershell
ffmpeg -version
# Should show version info
```

## Step 3: Clone/Download Project

```powershell
cd C:\path\to\projects
# If using git:
git clone <your-repo-url> meeting-intelligence-assistant
cd meeting-intelligence-assistant
```

## Step 4: Create Virtual Environment (Optional but Recommended)

```powershell
python -m venv venv
# Activate:
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 5: Install Python Dependencies

```powershell
cd C:\path\to\meeting-intelligence-assistant
pip install -r requirements.txt
```

This will install ~73 packages including:
- FastAPI, Uvicorn (backend)
- Streamlit (frontend)
- SQLAlchemy (ORM)
- faster-whisper (transcription)
- pydantic (validation)
- And more...

**Installation takes 10-15 minutes** depending on internet speed.

**Verify:**
```powershell
pip list | findstr "fastapi streamlit sqlalchemy"
```

## Step 6: Create .env File

```powershell
cp .env.example .env
```

Edit `.env` with your configuration:

### Minimal Configuration (Local Only)

```
APP_NAME=Meeting Intelligence Assistant
APP_ENV=development
DEBUG=false
LOG_LEVEL=INFO

TRANSCRIPTION_PROVIDER=faster_whisper
TRANSCRIPTION_MODEL=base
LLM_PROVIDER=claude
FEATURE_LOCAL_ONLY_MODE=true
```

### With Claude API

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
LLM_PROVIDER=claude
LLM_MODEL=claude-3-5-sonnet-20241022
```

### With OpenAI

```
OPENAI_API_KEY=sk-your-key-here
OPENAI_WHISPER_MODEL=whisper-1
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
```

## Step 7: Initialize Database

```powershell
python -c "from app.core import init_db; init_db(); print('Database initialized')"
```

Should create `data/mia.db` with all tables.

## Step 8: Download Transcription Model (Optional)

The first time you use transcription, faster-whisper will download the model (~1 GB for 'base').

To pre-download:
```powershell
python -c "from faster_whisper import WhisperModel; model = WhisperModel('base'); print('Model cached')"
```

**Time**: 5-10 minutes depending on connection
**Space**: 1-2 GB for model files

## Step 9: Start the Application

### Using the Batch File (Easiest)

```powershell
run_windows.bat
```

This will:
1. Check Python installation
2. Create required directories
3. Install missing dependencies
4. Start FastAPI backend
5. Start Streamlit frontend

### Manual Start

Terminal 1 - Start Backend:
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Start Frontend:
```powershell
streamlit run app\ui\streamlit_app.py
```

## Step 10: Access the Application

Open your browser:
- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## Troubleshooting

### Python not found
```powershell
# Check Python is in PATH
python --version

# If not found, add to PATH:
# Windows Settings → Environment Variables → Add Python installation directory
```

### FFmpeg not found
```powershell
ffmpeg -version
# If not found, install FFmpeg and add to PATH
```

### pip install fails
```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Try installing requirements again
pip install -r requirements.txt --upgrade
```

### Port 8000 already in use
```powershell
# Kill the process using port 8000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Or use a different port:
python -m uvicorn app.main:app --port 8001
```

### Streamlit cache errors
```powershell
# Clear Streamlit cache
streamlit cache clear
```

### Database locked
```powershell
# Delete database and reinitialize
del data\mia.db
python -c "from app.core import init_db; init_db()"
```

### Import errors
```powershell
# Verify virtual environment is activated
# Install dependencies again
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

## Development Setup

If you're developing/contributing:

```powershell
# Install with development dependencies
pip install -r requirements.txt

# Install code quality tools
pip install black flake8 mypy isort

# Format code
black app/
isort app/

# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=app --cov-report=html
```

## Next Steps

1. Upload a meeting recording
2. Review the transcript
3. Generate analysis
4. Export a report

See [README.md](README.md) for usage guide.

## Getting Help

- Check logs in `logs/mia.log`
- Read [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
- Review [SECURITY.md](docs/SECURITY.md) for security settings
- Check [GitHub Issues](https://github.com) for known problems

---

**Installation complete!** You're ready to use Meeting Intelligence Assistant.
