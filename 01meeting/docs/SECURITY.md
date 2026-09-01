# Security and Privacy Guide

## Overview

The Meeting Intelligence Assistant is designed with security and privacy as foundational principles. This document details security controls, privacy measures, and compliance considerations.

## Secret Management

### API Keys

**NEVER**:
- Commit API keys to version control
- Hard-code keys in source code
- Include keys in logging or error messages
- Share keys via email or chat

**DO**:
- Store keys in `.env` (do not commit)
- Use environment variables
- Use Windows Credential Manager (future enhancement)
- Rotate keys regularly
- Use service-specific keys with minimal scope

### Configuration Example

```bash
# .env (do not commit)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxx
TEAMS_CLIENT_SECRET=xxxxxxxxxxxxxooooo
```

```python
# Code (always safe)
from app.core import settings

api_key = settings.anthropic_api_key  # Loaded from environment
```

### Windows Credential Manager (Future)

```python
# Future enhancement for secure credential storage
import keyring

def get_api_key(service_name: str, key_name: str) -> str:
    return keyring.get_password(service_name, key_name)
```

## File Upload Security

### Validation Checks

1. **MIME Type Verification**
   ```python
   ALLOWED_AUDIO_MIMES = {
       'audio/wav', 'audio/mpeg', 'audio/mp4', 'audio/ogg'
   }
   ALLOWED_VIDEO_MIMES = {
       'video/mp4', 'video/quicktime', 'video/x-msvideo'
   }
   ```

2. **File Size Limits**
   ```python
   MAX_UPLOAD_SIZE = 5000 * 1024 * 1024  # 5 GB
   CHUNK_SIZE = 1024 * 1024  # 1 MB
   ```

3. **Path Traversal Prevention**
   ```python
   import os
   safe_path = os.path.normpath(os.path.join(upload_dir, filename))
   if not safe_path.startswith(upload_dir):
       raise ValueError("Path traversal detected")
   ```

4. **Filename Sanitization**
   ```python
   import re
   safe_name = re.sub(r'[^\w\s.-]', '', filename)
   safe_name = safe_name[:255]  # Limit length
   ```

5. **Hash Verification (Duplicate Detection)**
   ```python
   import hashlib
   
   def calculate_file_hash(file_path: str) -> str:
       sha256_hash = hashlib.sha256()
       with open(file_path, "rb") as f:
           for chunk in iter(lambda: f.read(4096), b""):
               sha256_hash.update(chunk)
       return sha256_hash.hexdigest()
   ```

## Data Storage Security

### SQLite (MVP)

```python
# SQLite best practices
DATABASE_URL = "sqlite:///./data/mia.db"

# Set secure file permissions (Unix-like)
os.chmod("data/mia.db", 0o600)  # Read/write for owner only
```

### PostgreSQL (Enterprise)

```python
# PostgreSQL security
DATABASE_URL = "postgresql://user:password@host/dbname"

# Connection security
SQLALCHEMY_ENGINE_OPTIONS = {
    "connect_args": {
        "sslmode": "require",  # Force SSL
    }
}
```

### File Storage Security

```
data/
├── uploads/          # 0700 (rwx------)
├── transcripts/      # 0700 (rwx------)
├── reports/          # 0700 (rwx------)
├── models/           # 0755 (rwxr-xr-x)
└── mia.db           # 0600 (rw-------)
```

## Sensitive Data Handling

### What NOT to Log

```python
import logging

logger = logging.getLogger(__name__)

# ❌ BAD: Logs API keys
logger.info(f"Using API key: {api_key}")

# ✓ GOOD: Redact sensitive data
logger.info(f"Using API key: {api_key[:10]}...")

# ✓ GOOD: Log only non-sensitive details
logger.info(f"Calling LLM API (provider: claude, model: claude-3-5-sonnet)")
```

### Sensitive Data Classification

**Highly Sensitive** (Never log):
- API keys, tokens, credentials
- User passwords, OAuth tokens
- Personal identification numbers (SSN, passport)
- Credit card numbers
- Encryption keys

**Sensitive** (Log with redaction):
- User email addresses
- File names containing participant names
- Meeting titles with confidential markers
- Partial timestamps

**Non-sensitive** (Safe to log):
- Processing status (completed, failed)
- Token counts and API call counts
- Model names and configurations
- General error categories

### Redaction Utility

```python
def redact_api_key(key: str, show_chars: int = 10) -> str:
    """Redact API key to first N characters."""
    if len(key) <= show_chars:
        return "***"
    return key[:show_chars] + "***"

def redact_transcript_snippet(text: str, max_chars: int = 100) -> str:
    """Truncate and redact transcript snippets."""
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text
```

## Data Retention and Deletion

### Retention Policy

```python
# .env configuration
DATA_RETENTION_DAYS = 90  # Default: 90 days

# Automatic cleanup (nightly job)
def cleanup_expired_meetings():
    expiry_date = datetime.utcnow() - timedelta(days=settings.data_retention_days)
    meetings = db.query(Meeting).filter(
        Meeting.created_at < expiry_date,
        Meeting.is_deleted == False
    ).all()
    
    for meeting in meetings:
        soft_delete_meeting(meeting)
```

### Soft Delete (Audit Trail)

```python
# Database model
class Meeting(Base, SoftDeleteMixin):
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    deleted_by_id: Optional[int] = None

# Soft delete operation
def soft_delete_meeting(meeting: Meeting, deleted_by: User):
    meeting.is_deleted = True
    meeting.deleted_at = datetime.utcnow()
    meeting.deleted_by_id = deleted_by.id
    db.add(meeting)
    db.commit()
```

### Permanent Deletion (User-Initiated)

```python
@app.delete("/api/v1/meetings/{meeting_id}/permanently")
async def permanently_delete_meeting(meeting_id: int, current_user: User):
    """
    Permanently delete a meeting and all associated data.
    This action is irreversible.
    """
    meeting = db.query(Meeting).get(meeting_id)
    
    # Verify ownership
    if meeting.created_by_id != current_user.id:
        raise PermissionDenied()
    
    # Delete files
    for media_file in meeting.media_files:
        os.remove(media_file.file_path)
    
    # Delete database records (hard delete)
    db.delete(meeting)
    db.commit()
    
    # Audit log
    audit_log(
        user_id=current_user.id,
        action="permanently_delete_meeting",
        entity_type="Meeting",
        entity_id=meeting_id
    )
```

### Temporary File Cleanup

```python
import tempfile
import shutil

def cleanup_temp_files():
    """Clean up temporary processing files."""
    temp_dir = Path(settings.temp_dir)
    
    for file_path in temp_dir.glob("*"):
        try:
            if file_path.is_file():
                file_path.unlink()
            elif file_path.is_dir():
                shutil.rmtree(file_path)
        except Exception as e:
            logger.error(f"Failed to delete {file_path}: {e}")

# Schedule cleanup
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_temp_files, 'interval', hours=6)
scheduler.start()
```

## Logging Security

### Log Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

# Create secure logger
logger = logging.getLogger(__name__)

# Rotate logs to prevent unbounded growth
handler = RotatingFileHandler(
    settings.log_file,
    maxBytes=settings.log_file_size_mb * 1024 * 1024,
    backupCount=settings.log_backup_count
)

# Set permissions on log file
os.chmod(settings.log_file, 0o600)

# Use JSON logging for easier parsing/monitoring
formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### Audit Logging

```python
class AuditLog(Base, TimestampMixin):
    """Track all user actions for security."""
    user_id: int
    action: str  # upload, download, delete, edit, analyze
    entity_type: str  # Meeting, Transcript, ActionItem
    entity_id: int
    ip_address: str
    user_agent: str
    changes: dict  # What changed
    timestamp: datetime

# Log every significant action
def audit_log(
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int,
    changes: dict = None,
    request = None
):
    log_entry = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        ip_address=request.client.host if request else None,
        user_agent=request.headers.get("user-agent") if request else None,
        changes=changes or {},
        created_at=datetime.utcnow()
    )
    db.add(log_entry)
    db.commit()
```

## API Security

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

# Allow only trusted origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Streamlit dev
        "http://localhost:3000",  # React dev
        # "https://yourapp.com"  # Production
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)
```

### Request Validation

```python
from pydantic import BaseModel, Field, validator

class MeetingUploadRequest(BaseModel):
    file: bytes = Field(..., max_length=5000 * 1024 * 1024)
    title: str = Field(..., min_length=1, max_length=500)
    
    @validator('title')
    def title_safe(cls, v):
        # Prevent XSS via title
        if '<' in v or '>' in v or '"' in v:
            raise ValueError('Invalid characters in title')
        return v
```

## Microsoft Teams Integration Security

### OAuth 2.0 Flow

```
1. User clicks "Connect Teams"
   ↓
2. App redirects to Azure Entra ID login
   └─ client_id: registered app ID
   └─ redirect_uri: https://youapp.com/callback
   └─ scope: Calendars.Read, OnlineMeetings.Read
   ↓
3. User authenticates and grants permissions
   ↓
4. Azure returns authorization code
   ↓
5. App exchanges code for access token (backend)
   └─ Uses client_secret (never exposed to browser)
   ↓
6. Store refresh token securely (encrypted)
   ↓
7. Use access token for Microsoft Graph calls
```

### Scope Minimization

```python
# Request only required scopes
TEAMS_SCOPES = [
    "https://graph.microsoft.com/Calendars.Read",      # Read calendar
    "https://graph.microsoft.com/OnlineMeetings.Read",  # Read meeting details
    "https://graph.microsoft.com/Files.Read",           # Read transcripts
]

# NEVER request:
# - Mail.Read (not needed)
# - User.Read.All (too broad)
# - Directory.Read.All (too broad)
```

### Token Storage

```python
from cryptography.fernet import Fernet

class TeamsOAuthToken(Base):
    """Store Teams OAuth tokens securely."""
    user_id: int
    access_token: bytes  # Encrypted
    refresh_token: bytes  # Encrypted
    expires_at: datetime
    
    @staticmethod
    def encrypt_token(token: str, encryption_key: bytes) -> bytes:
        cipher = Fernet(encryption_key)
        return cipher.encrypt(token.encode())
    
    @staticmethod
    def decrypt_token(encrypted_token: bytes, encryption_key: bytes) -> str:
        cipher = Fernet(encryption_key)
        return cipher.decrypt(encrypted_token).decode()
```

## Consent and Privacy Notices

### Recording Consent

```python
# User must confirm this before processing meetings
CONSENT_NOTICE = """
⚠️  IMPORTANT: User Consent Required

Before using this application to process meeting recordings:

1. Ensure you have recorded or obtained consent from ALL meeting participants
2. Verify compliance with your organization's recording policies
3. Confirm legal compliance with applicable data protection laws
   (GDPR, CCPA, etc.)
4. Ensure confidential meetings are marked as such

The application processes and analyzes meeting content. Recordings may be
transcribed and analyzed for intelligence extraction.

User responsibility: You are solely responsible for obtaining necessary
consent and ensuring legal compliance.
"""

# Application startup check
def check_user_consent():
    if not user_has_accepted_consent():
        show_consent_dialog(CONSENT_NOTICE)
        if not user.confirms_consent():
            exit()
```

### Data Processing Agreement

```markdown
# Data Processing Terms

## What We Process
- Audio/video files you upload
- Transcripts you provide
- Meeting metadata (title, date, participants)

## How We Process
- Local transcription (no data sent to cloud) - Optional
- Cloud transcription via OpenAI - Only if you enable it
- Analysis via LLM (Claude/OpenAI) - Only if you enable it

## Who Can Access
- Only you (single-user MVP)
- Team members (if deployed to shared server)
- Never shared with third parties

## Data Retention
- Default: 90 days from creation
- You can delete immediately
- Hard delete available (irreversible)

## Your Rights
- Access all your data anytime
- Download data in JSON format
- Delete data permanently
- Opt out of cloud processing
```

## Testing Security

### Example Test Cases

```python
# tests/test_security.py
import pytest

def test_api_key_not_in_logs(caplog):
    """Ensure API keys are never logged."""
    api_key = "sk-test-xxxx1234"
    
    try:
        call_llm_api(api_key)
    except:
        pass
    
    # Check logs for exposed key
    for record in caplog.records:
        assert api_key not in record.message
        assert "***" in record.message or api_key[:10] in record.message

def test_file_upload_path_traversal():
    """Prevent path traversal attacks."""
    malicious_filename = "../../etc/passwd"
    
    with pytest.raises(ValueError):
        sanitize_filename(malicious_filename)

def test_sql_injection_prevention():
    """Ensure ORM prevents SQL injection."""
    malicious_input = "'; DROP TABLE users; --"
    
    # Should be safe due to parameterized queries
    results = db.query(User).filter(
        User.name == malicious_input
    ).all()
    
    assert len(results) == 0  # No users with that name
    # Table still exists (not dropped)
    assert db.query(User).first() is not None

def test_xss_prevention():
    """Prevent XSS attacks."""
    xss_payload = "<script>alert('xss')</script>"
    
    # Should be sanitized
    safe_title = sanitize_html(xss_payload)
    
    assert "<script>" not in safe_title
    assert "alert" not in safe_title
```

## Compliance Checklists

### GDPR Compliance
- [ ] Data processing agreement in place
- [ ] User consent collection
- [ ] Data access capabilities
- [ ] Data deletion capabilities
- [ ] Privacy policy published
- [ ] Right to rectification implemented
- [ ] Right to be forgotten (deletion) implemented
- [ ] Breach notification process defined

### CCPA Compliance
- [ ] Disclosure of data collection
- [ ] Right to know
- [ ] Right to delete
- [ ] Right to opt-out
- [ ] Non-discrimination for exercising rights

## Incident Response

### Potential Security Issues

| Issue | Detection | Response |
|-------|-----------|----------|
| API key exposed in logs | Search logs for patterns | Rotate key, clear logs |
| Unauthorized access | Audit log spike | Disable account, audit changes |
| File upload malware | Antivirus scan results | Quarantine, alert user |
| Database compromise | Integrity checks fail | Restore from backup |
| DDoS attack | Rate limit exceeded | Enable rate limiting |

### Incident Log

```python
class SecurityIncident(Base):
    incident_type: str  # api_key_exposed, unauthorized_access, etc
    severity: str  # critical, high, medium, low
    description: str
    detected_at: datetime
    resolved_at: Optional[datetime]
    response_actions: str
    root_cause: Optional[str]
    prevention: Optional[str]
```

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Secure File Upload](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
- [GDPR Compliance](https://gdpr-info.eu/)
- [CCPA Compliance](https://oag.ca.gov/privacy/ccpa)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [SQLAlchemy Security](https://docs.sqlalchemy.org/en/20/faq/security.html)
