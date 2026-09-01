# Meeting Intelligence Assistant - Solution Overview

## Project Vision
A production-ready Windows application that converts recorded meetings into actionable intelligence: transcripts, decisions, action items, and risks—with evidence-based summaries and expert-friendly exports.

## Key Design Principles
- **Evidence-grounded**: Every decision, action, and risk tied to a transcript timestamp and quote
- **No fabrication**: Missing data marked as "Unassigned," "TBD," or "Unknown"—never inferred
- **Modular providers**: Transcription, diarization, and LLM are pluggable for local or cloud
- **Secure by default**: Local-only mode, secrets in environment variables, audit logging, data retention controls
- **Enterprise-ready**: SQLite MVP with PostgreSQL-compatible schemas; Streamlit UI upgradeable to React

## Development Roadmap

### Stage 1: Architecture & Setup ✓
- Project structure
- Dependencies and environment
- SQLAlchemy models
- Pydantic schemas

### Stage 2: Core MVP
- File upload and validation
- FFmpeg audio extraction
- Local transcription (faster-whisper)
- Transcript storage and viewer

### Stage 3: AI Intelligence
- LLM provider abstraction (Claude, OpenAI-compatible)
- Structured analysis (summaries, decisions, actions, risks)
- Long-meeting chunking with map-reduce
- Token tracking and cost estimation

### Stage 4: User Interface
- Streamlit dashboard
- Transcript editor with speaker correction
- Action item tracker
- Settings management

### Stage 5: Reports & Exports
- DOCX, PDF, CSV, JSON, Markdown
- Email-ready summaries
- Transcript cleanup

### Stage 6: Teams Integration
- Transcript file upload (VTT, DOCX, TXT)
- Microsoft Graph OAuth (Phase 2, feature-flagged)
- Admin configuration guide

### Stage 7: Hardening
- Security controls and file validation
- Performance optimization
- Comprehensive tests
- Windows packaging
- Complete documentation

## Success Criteria
- Runs on Windows with `run_windows.bat`
- Uploads and transcribes a Teams recording
- Generates accurate summaries, decisions, and action items with evidence
- Exports professional reports
- Local-only operation without API keys
- Core workflows tested
- Documented and ready for another developer
