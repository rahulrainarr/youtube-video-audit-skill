# Stage 2: Core MVP - IN PROGRESS

## Overview

Stage 2 implements the core MVP: file upload, media processing (FFmpeg), transcription, and basic transcript management.

## Completed Components

### 1. ✅ File Utilities (`app/utils/file_utils.py`)

**Functions**:
- `calculate_file_hash()` - SHA256 for duplicate detection
- `validate_mime_type()` - MIME type checking
- `validate_file_extension()` - Extension validation
- `sanitize_filename()` - Remove invalid characters and path components
- `validate_file_path()` - Prevent directory traversal attacks
- `validate_upload_file()` - Comprehensive file validation
- `get_safe_path()` - Generate safe file paths
- `delete_file()` - Safe file deletion
- `get_audio_format_from_path()` - Extract format from filename

**Security**:
- Path traversal protection
- Filename sanitization
- MIME type validation
- File size limits
- Duplicate detection via hash

### 2. ✅ FFmpeg Utilities (`app/utils/ffmpeg_utils.py`)

**Functions**:
- `is_ffmpeg_available()` - Detect FFmpeg installation
- `get_media_info()` - Extract metadata using ffprobe
- `extract_audio()` - Convert video to audio (WAV, MP3, FLAC)
- `convert_audio()` - Convert between audio formats
- `get_audio_duration()` - Get duration in seconds
- `validate_audio_file()` - Verify audio integrity
- `split_audio()` - Split long audio into segments (future use)

**Features**:
- Automatic format detection
- Configurable sample rate
- Mono conversion
- Timeout handling (1 hour limit)
- Comprehensive error messages

### 3. ✅ Repository Pattern (`app/repositories/`)

**Base Repository** (`base.py`):
- CRUD operations (create, read, update, delete)
- Soft delete support
- Pagination
- Filtering
- Counting
- Ordering

**Meeting Repository** (`meeting.py`):
- `get_user_meetings()` - User-specific meetings
- `get_by_status()` - Filter by processing status
- `get_by_source()` - Filter by source (upload, Teams, etc.)
- `get_pending_processing()` - Meetings awaiting processing
- `search_by_title()` - Full-text search
- `get_recent()` - Most recent meetings
- `get_total_duration()` - Aggregate duration
- `update_status()` - Update processing status
- `update_processing_error()` - Log errors

**Media File Repository** (`media_file.py`):
- `get_by_meeting()` - All files for a meeting
- `get_by_hash()` - Duplicate detection
- `get_by_type()` - Filter by file type
- `get_original_files()` - Original uploads only
- `get_processed_files()` - Converted files
- `get_total_size()` - Aggregate file size
- `get_converted_files()` - Track conversions

### 4. ✅ Transcription Service Architecture

**Base Provider** (`transcription/base.py`):
- Abstract `TranscriptionProvider` class
- `TranscriptSegment` dataclass
- `TranscriptionResult` dataclass
- Timestamp formatting
- Segment merging utilities

**Faster-Whisper Provider** (`transcription/faster_whisper_provider.py`):
- Local transcription without cloud APIs
- Auto-detect device (CPU, CUDA, MPS)
- Configurable model size (tiny→large)
- Language detection and configuration
- Quantization support for low RAM
- Async/await support
- Progress tracking ready

**Features**:
- 7 supported audio formats
- Word-level timestamps
- Confidence scoring
- Language detection
- Device auto-detection
- Model caching

### 5. ✅ Meeting Service (`app/services/meeting_service.py`)

**Methods**:
- `create_meeting()` - Create new meeting record
- `store_media_file()` - Upload and validate file
- `extract_audio_from_video()` - FFmpeg integration
- `get_meeting_with_files()` - Load meeting + files
- `cleanup_temp_files()` - Temporary file management
- `mark_meeting_processing()` - Status updates
- `mark_meeting_completed()` - Success marking
- `mark_meeting_failed()` - Error logging

**Features**:
- Duplicate detection
- File validation
- Audio extraction
- Metadata extraction
- Temp file cleanup
- Error tracking

### 6. ✅ API Endpoints (`app/api/endpoints/meetings.py`)

**Endpoints**:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/meetings/` | List all meetings |
| GET | `/api/v1/meetings/{meeting_id}` | Get specific meeting |
| POST | `/api/v1/meetings/create` | Create new meeting |
| POST | `/api/v1/meetings/{meeting_id}/upload` | Upload file |
| POST | `/api/v1/meetings/{meeting_id}/extract-audio` | Extract audio from video |
| DELETE | `/api/v1/meetings/{meeting_id}` | Soft delete meeting |

**Features**:
- File validation
- MIME type checking
- Temp file handling
- Safe paths
- Error handling
- Duplicate detection

### 7. ✅ Testing Foundation (`tests/unit/test_file_utils.py`)

**Test Classes**:
- `TestSanitizeFilename` - 4 tests
- `TestValidateFileExtension` - 3 tests
- `TestValidateFilePath` - 3 tests
- `TestGetSafePath` - 2 tests
- `TestCalculateFileHash` - 3 tests

**Test Coverage**:
- Security (path traversal, injection)
- Validation logic
- Edge cases (long filenames, no extension)
- Hash consistency

## What Remains in Stage 2

### Transcription Integration

1. **Transcription Endpoints**:
   - POST `/api/v1/meetings/{meeting_id}/transcribe` - Start transcription
   - GET `/api/v1/meetings/{meeting_id}/transcription-status` - Progress polling
   - GET `/api/v1/transcripts/{transcript_id}` - Get transcript
   - PUT `/api/v1/transcripts/{transcript_id}` - Edit transcript

2. **Background Job Processing**:
   - Job queue for long-running transcription
   - Progress tracking
   - Retry logic
   - Cancellation support

3. **Transcript Storage**:
   - Store transcript segments
   - Preserve timestamps and speaker info
   - Handle speaker diarization data

### Transcript Viewer

1. **Update Streamlit UI** (`app/ui/streamlit_app.py`):
   - Implement transcript view page
   - Speaker label display
   - Search functionality
   - Inline editing (mark segments)

2. **Transcript Editor**:
   - Edit segment text
   - Rename speakers
   - Manual speaker correction

## Architecture Implementation

```
┌─ File Upload ──────────┐
│                        │
│ validate_upload_file() ├─── Check MIME, size, extension
│ get_safe_path()        ├─── Prevent path traversal
│ calculate_file_hash()  ├─── Detect duplicates
└────────────┬───────────┘
             │
             ▼
┌─ Store in Database ────┐
│                        │
│ MeetingRepository      ├─── Create meeting record
│ MediaFileRepository    ├─── Store file metadata
└────────────┬───────────┘
             │
             ▼
┌─ Process Media ────────┐
│                        │
│ extract_audio()        ├─── FFmpeg conversion
│ get_audio_duration()   ├─── Metadata extraction
└────────────┬───────────┘
             │
             ▼
┌─ Transcribe Audio ─────┐
│                        │
│ FastWhisperProvider    ├─── Local speech-to-text
│ TranscriptSegment[]    ├─── Time-bound segments
└────────────┬───────────┘
             │
             ▼
┌─ Store Transcript ─────┐
│                        │
│ TranscriptRepository   ├─── Save to database
│ TranscriptSegmentRepo  ├─── Store segments
└────────────────────────┘
```

## Validation Checklist

Run these commands to verify Stage 2 implementation:

```bash
# 1. Test imports
python -c "from app.services.transcription import FastWhisperProvider; print('✓ Transcription provider imports OK')"

# 2. Test repositories
python -c "from app.repositories import MeetingRepository, MediaFileRepository; print('✓ Repositories import OK')"

# 3. Test file utilities
python -c "from app.utils.file_utils import sanitize_filename, validate_upload_file; print('✓ File utils import OK')"

# 4. Test FFmpeg utilities
python -c "from app.utils.ffmpeg_utils import is_ffmpeg_available; print(f'✓ FFmpeg available: {is_ffmpeg_available()}')"

# 5. Run unit tests
pytest tests/unit/test_file_utils.py -v

# 6. Test API startup
python -m uvicorn app.main:app --help > /dev/null && echo "✓ API startup OK"

# 7. Test database initialization
python -c "from app.core import init_db; init_db(); print('✓ Database initialized')"
```

## Example Usage (Once Complete)

```bash
# 1. Start API
python -m uvicorn app.main:app --reload

# 2. In another terminal - Upload a meeting
curl -X POST "http://localhost:8000/api/v1/meetings/create" \
  -H "Content-Type: application/json" \
  -d '{"title": "Q3 Planning", "description": "Quarterly planning meeting"}'

# 3. Upload audio file
curl -X POST "http://localhost:8000/api/v1/meetings/1/upload" \
  -F "file=@recording.mp3"

# 4. Start transcription (when endpoint is complete)
curl -X POST "http://localhost:8000/api/v1/meetings/1/transcribe"

# 5. Check transcription status
curl "http://localhost:8000/api/v1/meetings/1/transcription-status"

# 6. Get transcript when complete
curl "http://localhost:8000/api/v1/transcripts/1"
```

## Next Steps

1. **Implement Background Job System**:
   - Job queue (using APScheduler or Celery)
   - Progress tracking
   - Error retry logic

2. **Complete Transcription Endpoints**:
   - Start transcription endpoint
   - Status polling endpoint
   - Transcript endpoints (GET, PUT)

3. **Implement Transcript Storage**:
   - TranscriptRepository
   - Segment storage
   - Speaker diarization integration

4. **Update Streamlit UI**:
   - Transcript viewer
   - Speaker editor
   - Search functionality

5. **Integration Testing**:
   - End-to-end file upload test
   - Transcription pipeline test
   - Database persistence test

## Estimated Completion

- **Transcription endpoints**: 1-2 hours
- **Background jobs**: 2 hours
- **Transcript storage**: 1 hour
- **Streamlit updates**: 1-2 hours
- **Testing and fixes**: 1-2 hours

**Total for Stage 2**: ~8 hours

## Dependencies Installed

✅ All requirements.txt packages available including:
- faster-whisper 0.10.0
- FFmpeg (separate system install required)
- SQLAlchemy 2.0.23
- FastAPI 0.104.1
- Streamlit 1.31.1
- Pydantic 2.5.0

---

**Status**: Stage 2 Core Foundation Complete
**Next**: Background job system and transcription endpoints
