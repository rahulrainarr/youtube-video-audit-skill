# Meeting Intelligence Assistant - Quick Start

## ✅ Fixed Issues

✓ Removed `sqlite3-python` (built into Python)
✓ Made optional packages optional (torch, pyannote, reporting libraries)
✓ Created lean, installable requirements.txt

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```powershell
cd C:\02 Claude\02 Code\01meeting
pip install -r requirements.txt
```
**Time**: 10-15 minutes (first time only)

### Step 2: Initialize Database
```powershell
python -c "from app.core import init_db; init_db(); print('✓ Database ready')"
```

### Step 3: Start Backend (Terminal 1)
```powershell
python -m uvicorn app.main:app --reload --port 8000
```
Output should show:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Step 4: Start Frontend (Terminal 2)
```powershell
streamlit run app/ui/streamlit_app.py
```
Output should show:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Step 5: Access Application
- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📋 What You Get

### Core Features Ready
✅ **File Upload** - Accept audio, video, transcripts
✅ **Audio Extraction** - FFmpeg integration for video→audio
✅ **Transcription** - Local (faster-whisper) or cloud (OpenAI)
✅ **Database** - 17 models with full relationships
✅ **API** - 6 documented endpoints
✅ **UI** - Streamlit with navigation

### Data Models (17 Total)
- User, Meeting, Participant
- MediaFile, Transcript, TranscriptSegment
- Summary, KeyPoint, Decision, ActionItem
- Risk, Issue, OpenQuestion
- ProcessingJob, ExportRecord, AuditLog, ApplicationSetting

### API Endpoints
```
GET    /api/v1/meetings/                    List meetings
GET    /api/v1/meetings/{id}                Get meeting
POST   /api/v1/meetings/create              Create meeting
POST   /api/v1/meetings/{id}/upload         Upload file
POST   /api/v1/meetings/{id}/extract-audio  Extract audio
DELETE /api/v1/meetings/{id}                Delete meeting
```

---

## 🔧 Configuration

### Local-Only Mode (Recommended for Testing)
Edit `.env`:
```
TRANSCRIPTION_PROVIDER=faster_whisper
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
```

---

## 🧪 Test the System

### Quick Test
```powershell
python test_demo.py
```

### Unit Tests
```powershell
pytest tests/unit/test_file_utils.py -v
```

---

## 📁 Project Structure

```
01meeting/
├── app/
│   ├── api/           # FastAPI endpoints
│   ├── models/        # 17 SQLAlchemy models
│   ├── schemas/       # Pydantic validation
│   ├── services/      # Business logic
│   ├── repositories/  # Data access
│   ├── ui/            # Streamlit frontend
│   ├── utils/         # File & FFmpeg utilities
│   ├── core/          # Config & database
│   └── main.py        # FastAPI app
├── tests/             # Unit tests
├── data/              # Data storage
│   ├── uploads/       # Uploaded files
│   ├── models/        # ML model cache
│   ├── temp/          # Temporary files
│   └── mia.db         # SQLite database
├── docs/              # Documentation
├── .env.example       # Configuration template
├── requirements.txt   # Dependencies (fixed)
└── README.md          # Full documentation
```

---

## 🆘 Troubleshooting

### Port Already in Use
```powershell
# Use different port
python -m uvicorn app.main:app --port 8001
```

### Streamlit Not Found
```powershell
pip install streamlit
```

### FFmpeg Not Found
```powershell
# Install FFmpeg
choco install ffmpeg

# Verify
ffmpeg -version
```

### Database Locked
```powershell
# Delete and recreate
Remove-Item data/mia.db
python -c "from app.core import init_db; init_db()"
```

---

## 📚 Documentation

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design (20+ pages)
- **[SECURITY.md](docs/SECURITY.md)** - Security guidelines (15+ pages)  
- **[README.md](README.md)** - Full documentation
- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Detailed setup

---

## ✨ Next Steps

1. **Run the application** (Steps 1-5 above)
2. **Upload a test file** via the UI
3. **Generate transcript** (local transcription)
4. **Edit and review** transcript
5. **Generate analysis** with AI
6. **Export report** (DOCX, PDF, JSON)

---

## 🎯 Success Checklist

- [ ] Dependencies installed (no errors)
- [ ] Database initialized (data/mia.db exists)
- [ ] API running (http://localhost:8000 responds)
- [ ] UI accessible (http://localhost:8501)
- [ ] Can upload file via UI
- [ ] Can view API docs (/docs)

---

**You're all set! Start with the 5-minute setup above.**

Questions? Check the docs or review the working demo in `test_demo.py`.
