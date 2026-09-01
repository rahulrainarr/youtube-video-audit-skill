# Meeting Intelligence Assistant

Convert recorded meetings into actionable intelligence: transcripts, decisions, action items, and comprehensive insights.

## Features

- **Audio & Video Processing**: Upload MP3, WAV, M4A, MP4, MOV, MKV with automatic audio extraction
- **Transcription**: Local (faster-whisper) or cloud (OpenAI Whisper API)
- **Speaker Diarization**: Identify and label speakers with manual correction capability
- **AI-Powered Intelligence**: Generate summaries, extract decisions, identify action items, risks, and issues
- **LLM Flexibility**: Support for Claude (Anthropic), OpenAI, and OpenAI-compatible APIs
- **Professional Reports**: Export as DOCX, PDF, Markdown, JSON, or CSV
- **Teams Integration**: Upload Teams-generated transcripts; Graph integration (Phase 2)
- **Local-Only Mode**: Process meetings entirely locally without cloud services
- **Evidence-Based**: Every insight backed by transcript timestamps and quotes

## System Requirements

- **OS**: Windows 11 (Windows 10 may work)
- **Python**: 3.12+
- **RAM**: 8GB+ (16GB recommended for local transcription)
- **Storage**: 50GB+ for models and data
- **FFmpeg**: Required for video processing

## Installation

### Step 1: Clone or Download the Project

```bash
cd C:\path\to\project
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `TRANSCRIPTION_PROVIDER` (faster_whisper or openai)
- `LLM_PROVIDER` (claude, openai, or openai_compatible)
- API keys if using cloud services

### Step 4: Install FFmpeg

**Option A: Using Chocolatey**
```powershell
choco install ffmpeg
```

**Option B: Manual Installation**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\Program Files\FFmpeg` or similar
3. Add to PATH: `C:\Program Files\FFmpeg\bin`

**Verify Installation:**
```bash
ffmpeg -version
```

### Step 5: Download Transcription Model (Local Mode)

If using `faster_whisper`, the model auto-downloads on first use:

```bash
python -c "from faster_whisper import WhisperModel; model = WhisperModel('base')"
```

## Running the Application

### Option 1: Using run_windows.bat

```batch
run_windows.bat
```

This starts both the FastAPI backend and Streamlit frontend.

### Option 2: Manual Start

**Terminal 1 - Start FastAPI:**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Streamlit:**
```bash
streamlit run app/ui/streamlit_app.py
```

Access the UI at: `http://localhost:8501`

## Configuration

### API Keys (Choose One)

**Claude API:**
```bash
set ANTHROPIC_API_KEY=your-key-here
set LLM_PROVIDER=claude
set LLM_MODEL=claude-3-5-sonnet-20241022
```

**OpenAI:**
```bash
set OPENAI_API_KEY=your-key-here
set OPENAI_WHISPER_MODEL=whisper-1
set LLM_PROVIDER=openai
set LLM_MODEL=gpt-4
```

**Local LLM (OpenAI-compatible):**
```bash
set OPENAI_LLM_API_BASE=http://localhost:8000/v1
set OPENAI_LLM_MODEL=local-model-name
set LLM_PROVIDER=openai_compatible
```

### Transcription Settings

**Local Transcription (faster-whisper):**
```bash
set TRANSCRIPTION_PROVIDER=faster_whisper
set TRANSCRIPTION_MODEL=base        # Options: tiny, base, small, medium, large
set TRANSCRIPTION_DEVICE=auto       # Options: auto, cpu, gpu, cuda, mps
set WHISPER_ENABLE_QUANTIZATION=true  # For lower RAM usage
```

**Cloud Transcription (OpenAI):**
```bash
set TRANSCRIPTION_PROVIDER=openai
set OPENAI_API_KEY=your-key-here
```

## Project Structure

```
meeting-intelligence-assistant/
├── app/
│   ├── api/                    # FastAPI endpoints
│   ├── core/                   # Configuration, database setup
│   ├── models/                 # SQLAlchemy ORM models
│   ├── schemas/                # Pydantic request/response schemas
│   ├── services/               # Business logic
│   │   ├── transcription/      # Transcription providers
│   │   ├── diarization/        # Speaker diarization
│   │   ├── llm/                # LLM providers
│   │   ├── teams/              # Teams integration
│   │   └── reporting/          # Report generation
│   ├── repositories/           # Data access layer
│   ├── workers/                # Background job processing
│   ├── ui/                     # Streamlit frontend
│   └── main.py                 # FastAPI application entry point
├── tests/                      # Unit and integration tests
├── data/                       # Data storage
│   ├── uploads/                # Uploaded files
│   ├── models/                 # ML models cache
│   ├── temp/                   # Temporary processing files
│   └── mia.db                  # SQLite database (created on first run)
├── docs/                       # Documentation
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
├── run_windows.bat             # Windows startup script
└── README.md                   # This file
```

## Architecture

### Processing Workflow

1. **File Upload** → Validate, hash, store metadata
2. **Media Processing** → Extract audio from video
3. **Transcription** → Convert audio to text (local or cloud)
4. **Diarization** → Identify speakers (optional)
5. **AI Analysis** → Generate intelligence via LLM
6. **Export** → Generate reports in various formats
7. **Cleanup** → Apply retention policy

### Provider Architecture

The application uses pluggable providers:

- **Transcription**: `faster_whisper`, `openai`
- **LLM**: `claude`, `openai`, `openai_compatible`
- **Diarization**: `pyannote.audio` (local)

## Data Storage

- **Database**: SQLite (MVP) → PostgreSQL (Enterprise)
- **Files**: Local filesystem with soft-delete support
- **Models**: Cached in `data/models/`
- **Logs**: `logs/mia.log`

## Security

- **No API keys in code**: Use environment variables or Windows Credential Manager
- **Soft delete**: Data marked deleted, not permanently removed
- **Audit logging**: All actions tracked
- **Local-only mode**: Process meetings without cloud services
- **File validation**: MIME type checks, size limits, path traversal prevention

## Troubleshooting

### FFmpeg Not Found
```powershell
# Check installation
ffmpeg -version

# Add to PATH (PowerShell admin)
$env:Path += ";C:\Program Files\FFmpeg\bin"
```

### API Key Issues
- Verify `.env` file exists and is readable
- Check API key has correct permissions
- Keys should not be committed to git

### Out of Memory
```bash
set WHISPER_ENABLE_QUANTIZATION=true
set TRANSCRIPTION_MODEL=tiny
set TRANSCRIPTION_DEVICE=cpu
```

### Database Locked
- Ensure only one instance is running
- Delete `data/mia.db-journal` if present

## Development

### Run Tests
```bash
pytest tests/ -v
```

### Code Quality
```bash
black app/
flake8 app/
mypy app/
```

### Create Migrations (PostgreSQL)
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Roadmap

- [x] Stage 1: Architecture & Setup
- [ ] Stage 2: Core MVP (File upload, transcription, storage)
- [ ] Stage 3: AI Intelligence (Summaries, decisions, actions)
- [ ] Stage 4: User Interface (Dashboard, editor, settings)
- [ ] Stage 5: Reports & Exports (DOCX, PDF, etc.)
- [ ] Stage 6: Teams Integration (Phase 2 with Graph)
- [ ] Stage 7: Hardening (Security, performance, tests, packaging)

## Support

For issues, feature requests, or questions:
1. Check the [ARCHITECTURE.md](docs/ARCHITECTURE.md) for design details
2. Review [SECURITY.md](docs/SECURITY.md) for security guidelines
3. See [Teams Integration Guide](docs/TEAMS_INTEGRATION.md) for Graph setup

## License

[To be defined]

## Change Log

### v1.0.0 (Initial Release)
- Stage 1: Project structure and core configuration
- SQLAlchemy data models
- Pydantic schemas
- FastAPI application skeleton
- Environment configuration
- Database initialization
