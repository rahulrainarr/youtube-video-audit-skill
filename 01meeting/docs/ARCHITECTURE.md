# Meeting Intelligence Assistant - Architecture

## System Overview

The Meeting Intelligence Assistant is a desktop application that processes meeting recordings and transcripts to generate actionable intelligence.

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interface (Streamlit)                   │
│  Dashboard | Uploads | Transcript Editor | Reports | Settings   │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   FastAPI REST Backend                          │
│  /api/v1/meetings  /api/v1/transcripts  /api/v1/analysis        │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              Core Application Services                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ File Processing                                          │  │
│  │ • Upload validation                                      │  │
│  │ • FFmpeg media extraction                                │  │
│  │ • Temporary file management                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Transcription Service (Pluggable)                        │  │
│  │ ├─ faster-whisper (local)                                │  │
│  │ └─ OpenAI Whisper API (cloud)                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Diarization Service (Optional)                           │  │
│  │ • Speaker identification                                 │  │
│  │ • Speaker label management                               │  │
│  │ • Manual correction persistence                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ LLM Service (Pluggable)                                  │  │
│  │ ├─ Claude (Anthropic)                                    │  │
│  │ ├─ OpenAI                                                │  │
│  │ └─ OpenAI-compatible API                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Analysis Engine                                          │  │
│  │ • Transcript chunking (map-reduce)                       │  │
│  │ • Intelligence extraction                                │  │
│  │ • Result consolidation & deduplication                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Report Generation                                        │  │
│  │ • DOCX, PDF, CSV, JSON, Markdown                         │  │
│  │ • Email summaries                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Teams Integration (Phase 1 & 2)                          │  │
│  │ • Transcript upload & parsing                            │  │
│  │ • Microsoft Graph API (Phase 2)                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                  Data Layer (SQLAlchemy)                        │
│                                                                 │
│  SQLite (MVP) ──────────────────────────► PostgreSQL (Prod)    │
│                                                                 │
│  • Users                    • ActionItems                        │
│  • Meetings                 • Risks                              │
│  • Participants             • Issues                             │
│  • MediaFiles               • OpenQuestions                      │
│  • Transcripts              • ExportRecords                      │
│  • Summaries                • ProcessingJobs                     │
│  • KeyPoints                • AuditLogs                          │
│  • Decisions                • Settings                           │
└─────────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    File Storage                                 │
│                                                                 │
│  data/uploads/     - Uploaded media files                       │
│  data/transcripts/ - Extracted transcripts                      │
│  data/reports/     - Generated reports                          │
│  data/exports/     - Export files                               │
│  data/models/      - ML model cache                             │
│  data/temp/        - Temporary processing files                 │
│  logs/             - Application logs                           │
└─────────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. File Upload & Validation

**Location**: `app/services/file_processing/`

**Responsibilities**:
- Accept audio, video, and transcript files
- Validate file type, size, and integrity
- Generate file hash for duplicate detection
- Extract audio from video using FFmpeg
- Store files with safe naming

**Supported Formats**:
- Audio: WAV, MP3, M4A, AAC, FLAC, OGG
- Video: MP4, MOV, MKV, WEBM, AVI, FLV
- Transcripts: VTT, SRT, TXT, DOCX

### 2. Transcription Service

**Location**: `app/services/transcription/`

**Architecture**:
```python
class TranscriptionProvider(ABC):
    async def transcribe(self, audio_path: str) -> TranscriptSegments
    async def get_language(self) -> str
    async def get_model_info(self) -> ModelInfo

class FastWhisperProvider(TranscriptionProvider):
    # Local CPU/GPU transcription using faster-whisper

class OpenAIProvider(TranscriptionProvider):
    # Cloud transcription via OpenAI Whisper API
```

**Features**:
- Token-aware chunking for long audio
- Automatic language detection
- Word-level timestamps
- Confidence scores
- Voice activity detection
- Quantization support for lower memory

### 3. Speaker Diarization

**Location**: `app/services/diarization/`

**Approach**:
- Uses `pyannote.audio` for speaker segmentation
- Assigns speaker labels (Speaker 1, Speaker 2, etc.)
- Allows manual speaker name corrections
- Preserves corrections across re-processing
- Marks uncertain attributions

**Data Flow**:
```
Transcript Segments (no speaker)
    ↓
[Diarization Model]
    ↓
Segments with Speaker Labels + Confidence
    ↓
[Manual Correction (optional)]
    ↓
Final Transcript with Speaker Names
```

### 4. LLM Service

**Location**: `app/services/llm/`

**Provider Abstraction**:
```python
class LLMProvider(ABC):
    async def generate(self, prompt: str, schema: Type[T]) -> T
    async def count_tokens(self, text: str) -> int
    async def estimate_cost(self, tokens_in: int, tokens_out: int) -> float

class ClaudeProvider(LLMProvider):
    # Anthropic Claude API

class OpenAIProvider(LLMProvider):
    # OpenAI GPT models

class OpenAICompatibleProvider(LLMProvider):
    # Local or third-party OpenAI-compatible endpoints
```

**Features**:
- Token counting for budget estimation
- Cost tracking for cloud APIs
- Retry logic with exponential backoff
- Request timeout handling
- Structured output validation (Pydantic)

### 5. Analysis Engine

**Location**: `app/services/analysis/`

**Processing Pipeline**:

```
Raw Transcript
    ↓
[Chunking Strategy]
    ├─ Token-aware chunks
    ├─ Preserve speaker continuity
    ├─ Overlap for context
    └─ Track timestamp ranges
    ↓
[Parallel LLM Calls]
    ├─ Summarize each chunk
    ├─ Extract decisions
    ├─ Extract action items
    ├─ Identify risks/issues
    └─ Collect questions
    ↓
[Consolidation]
    ├─ Deduplication
    ├─ Cross-chunk consistency check
    ├─ Timestamp mapping
    └─ Confidence aggregation
    ↓
Structured Meeting Intelligence (JSON)
```

**Long-Meeting Strategy** (> 1 hour):

1. **Chunking**: Split transcript maintaining speaker and timestamp context
2. **Map Phase**: Analyze each chunk independently
3. **Reduce Phase**: Consolidate results, remove duplicates
4. **Validation**: Cross-check for consistency

**Deduplication Rules**:
- Same action item appearing in multiple chunks → Merge with earliest evidence
- Contradictory decisions → Flag both with confidence levels
- Repeated risks → Combine with strongest evidence

### 6. Data Models

**Core Entities**:
- `User`: Application users
- `Meeting`: Recorded meeting metadata
- `Participant`: Meeting attendees
- `MediaFile`: Uploaded audio/video files
- `Transcript`: Full meeting transcript
- `TranscriptSegment`: Time-bound transcript sections
- `Summary`: Executive summaries
- `KeyPoint`: Discussion highlights
- `Decision`: Agreed decisions
- `ActionItem`: Tasks with owners and deadlines
- `Risk`: Identified risks
- `Issue`: Identified issues
- `OpenQuestion`: Unanswered questions
- `ProcessingJob`: Background job tracking
- `ExportRecord`: Generated reports
- `AuditLog`: User actions
- `ApplicationSetting`: Configuration

**Schema Design**:
- SQLite for MVP (file-based, no server)
- PostgreSQL-compatible schema for enterprise
- Soft-delete support for audit trail
- Timestamps (created_at, updated_at) on all entities
- Indexes on frequently queried columns

### 7. Report Generation

**Location**: `app/services/reporting/`

**Formats Supported**:
- **DOCX**: Professional meeting report with formatting
- **PDF**: Print-ready report
- **Markdown**: Text-based for version control
- **JSON**: Raw structured data
- **CSV**: Action items for spreadsheet import
- **VTT/SRT**: Subtitle formats for video sync

**Report Template**:
```
1. Cover Page (Meeting Title, Date, Duration)
2. Executive Summary (Bullets)
3. Key Points (With speakers and timestamps)
4. Decisions (With owners and rationale)
5. Action Items (Sortable by priority, owner, due date)
6. Risks and Issues (Impact assessment)
7. Open Questions
8. Next Steps
9. Appendix (Full Transcript)
```

### 8. Background Job Processing

**Location**: `app/workers/`

**Purpose**: Handle long-running tasks asynchronously

**Job Types**:
- Transcription
- Diarization
- Analysis
- Report generation

**Monitoring**:
- Real-time progress updates
- Cancellation support
- Retry logic for failures
- Cost/token tracking

## Processing Workflow

### End-to-End Meeting Processing

```
1. USER UPLOADS FILE
   ├─ Validate file (size, type, integrity)
   ├─ Generate file hash (detect duplicates)
   ├─ Create Meeting record
   └─ Store MediaFile record
   Status: PENDING

2. EXTRACT AUDIO (if video)
   ├─ Invoke FFmpeg
   ├─ Convert to WAV/FLAC
   ├─ Validate audio properties
   └─ Store converted file
   Status: PROCESSING

3. TRANSCRIBE
   ├─ Split audio into safe chunks (5-15 min)
   ├─ Call transcription provider
   ├─ Merge results maintaining timestamps
   ├─ Create Transcript record
   └─ Store TranscriptSegments
   Status: TRANSCRIBING

4. DIARIZE (optional)
   ├─ Run diarization model
   ├─ Assign speaker labels
   ├─ Create initial speaker-to-name mapping
   └─ Update TranscriptSegments
   Status: DIARIZING

5. ALLOW TRANSCRIPT REVIEW
   ├─ User views transcript
   ├─ User corrects speaker names
   ├─ User edits text (if needed)
   └─ Save corrections to database
   Status: REVIEWING

6. ANALYZE
   ├─ Chunk transcript intelligently
   ├─ Call LLM for summaries, decisions, actions, risks
   ├─ Deduplicate and consolidate results
   ├─ Validate structured output (Pydantic)
   ├─ Create Summary, Decision, ActionItem records
   └─ Allow user editing of results
   Status: ANALYZING

7. GENERATE REPORTS
   ├─ Select export format
   ├─ Generate report document
   └─ Store ExportRecord
   Status: COMPLETED

8. APPLY RETENTION POLICY
   ├─ Calculate retention expiry
   ├─ Mark old meetings for soft-delete
   └─ Archive or permanently delete per policy

9. AUDIT LOG
   └─ Record all actions taken
```

## Security Model

### Input Validation

- **File Upload**: MIME type check, size limit, path traversal prevention
- **Database**: SQL injection prevention via ORM
- **API**: Input validation via Pydantic
- **Transcript**: HTML/JavaScript sanitization

### Secret Management

- API keys stored in environment variables only
- No secrets in code or logs
- Windows Credential Manager integration (future)
- Encrypted storage ready (field-level encryption)

### Access Control

- User authentication (basic for MVP)
- Soft-delete for audit trail
- Audit logging of all actions
- IP logging for security events

### Data Privacy

- Local-only mode (no cloud calls)
- Data retention policies
- Permanent deletion support
- GDPR-ready architecture

## Deployment Scenarios

### Scenario 1: Local Development

- Backend: `uvicorn app.main:app --reload`
- Frontend: `streamlit run app/ui/streamlit_app.py`
- Database: SQLite at `data/mia.db`
- Storage: Local filesystem

### Scenario 2: Single-User Windows Desktop

- Run via `run_windows.bat`
- All processing local (no cloud APIs required)
- SQLite database
- Secure credential storage

### Scenario 3: Team Server (PostgreSQL)

- FastAPI running in production
- PostgreSQL for multi-user support
- Shared file storage (NAS or cloud)
- HTTPS with OAuth 2.0
- Teams Graph integration enabled

### Scenario 4: Cloud Deployment

- Kubernetes cluster
- PostgreSQL managed database
- S3/GCS for file storage
- Azure/Google Cloud authentication
- Horizontal scaling of workers

## Performance Considerations

### Memory Usage

- **Transcription**: 2-6 GB (depends on model size)
- **Diarization**: 1-2 GB
- **LLM calls**: Stream responses to avoid buffering
- **Chunking**: Process one chunk at a time

### CPU/GPU

- Auto-detect CUDA availability
- GPU acceleration for transcription/diarization
- Fallback to CPU with warnings
- Quantization for low-resource systems

### Concurrency

- Single transcription job per system
- Queue multiple meetings
- LLM calls in parallel (respecting rate limits)
- Background job max concurrency = 2 (configurable)

### Cost Estimation

- Track API calls and tokens per processing job
- Estimate cost before cloud transcription
- Alert user if cost exceeds threshold
- Show cost breakdown in reports

## Future Enhancements

### Phase 2: Microsoft Teams Integration

- OAuth 2.0 with Microsoft Entra ID
- Microsoft Graph API for meeting transcripts
- Automatic transcript retrieval
- Change notifications for new meetings

### Phase 3: Advanced Features

- Multi-language transcription
- Real-time meeting processing
- Custom vocabulary/domain terms
- ML model fine-tuning for accuracy
- Search across meetings
- Meeting comparison and trends

### Phase 4: Enterprise Scale

- Multi-tenancy support
- Advanced permission model
- SAML/OIDC authentication
- Audit trail compliance
- Encryption at rest and in transit
- Disaster recovery and HA setup
