"""API endpoints for meeting operations."""

import logging
import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import settings, get_db
from app.repositories import MeetingRepository
from app.services.meeting_service import MeetingService
from app.utils.file_utils import (
    validate_upload_file,
    get_safe_path,
    ensure_directory,
)
from app.schemas import MeetingSchema, MeetingCreateSchema

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.get("/")
async def list_meetings(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
):
    """List all meetings."""
    repo = MeetingRepository(db)
    meetings = repo.get_all(skip=skip, limit=limit)
    return {
        "total": repo.count(),
        "skip": skip,
        "limit": limit,
        "items": meetings,
    }


@router.get("/{meeting_id}")
async def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    """Get a specific meeting."""
    repo = MeetingRepository(db)
    meeting = repo.get(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.post("/create")
async def create_meeting(
    request: MeetingCreateSchema,
    user_id: int = 1,  # TODO: Get from auth
    db: Session = Depends(get_db),
):
    """Create a new meeting."""
    service = MeetingService(db)
    meeting = service.create_meeting(
        title=request.title,
        user_id=user_id,
        description=request.description,
        meeting_date=request.meeting_date,
        location=request.location,
        is_confidential=request.is_confidential,
    )
    return meeting


@router.post("/{meeting_id}/upload")
async def upload_meeting_file(
    meeting_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a file to a meeting."""
    try:
        # Verify meeting exists
        repo = MeetingRepository(db)
        meeting = repo.get(meeting_id)
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")

        # Read file content
        content = await file.read()
        file_size = len(content)

        # Determine file type based on extension
        file_lower = file.filename.lower()
        if any(file_lower.endswith(ext) for ext in [".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"]):
            file_type = "audio"
        elif any(file_lower.endswith(ext) for ext in [".mp4", ".mov", ".mkv", ".webm", ".avi", ".flv"]):
            file_type = "video"
        elif any(file_lower.endswith(ext) for ext in [".vtt", ".srt", ".txt", ".docx"]):
            file_type = "transcript"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Validate file
        temp_path = str(Path(settings.temp_dir) / f"temp_{uuid.uuid4().hex}")
        try:
            with open(temp_path, "wb") as f:
                f.write(content)

            valid, error = validate_upload_file(temp_path, file_size, file_type)
            if not valid:
                raise HTTPException(status_code=400, detail=error)

            # Move to permanent storage
            ensure_directory(settings.temp_dir)
            upload_dir = Path(settings.temp_dir) / "uploads"
            ensure_directory(str(upload_dir))

            safe_filename = f"{uuid.uuid4().hex}_{file.filename}"
            safe_path = get_safe_path(str(upload_dir), safe_filename)

            os.rename(temp_path, safe_path)

            # Store in database
            service = MeetingService(db)
            success, media_file, msg = service.store_media_file(
                meeting_id=meeting_id,
                file_path=safe_path,
                original_filename=file.filename,
                file_type=file_type,
                mime_type=file.content_type or "application/octet-stream",
            )

            if not success:
                raise HTTPException(status_code=400, detail=msg)

            return {
                "success": True,
                "message": "File uploaded successfully",
                "media_file_id": media_file.id,
                "file_name": media_file.file_name,
                "file_size": media_file.file_size_bytes,
            }

        finally:
            # Clean up temp file if it still exists
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")


@router.post("/{meeting_id}/extract-audio")
async def extract_audio(
    meeting_id: int,
    media_file_id: int,
    db: Session = Depends(get_db),
):
    """Extract audio from a video file."""
    try:
        service = MeetingService(db)
        success, audio_file, message = service.extract_audio_from_video(media_file_id)

        if not success:
            raise HTTPException(status_code=400, detail=message)

        return {
            "success": True,
            "message": message,
            "audio_file_id": audio_file.id,
            "duration_seconds": audio_file.duration_seconds,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting audio: {e}")
        raise HTTPException(status_code=500, detail=f"Extraction error: {str(e)}")


@router.delete("/{meeting_id}")
async def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    """Soft delete a meeting."""
    repo = MeetingRepository(db)
    meeting = repo.get(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    success = repo.soft_delete(meeting_id)
    if success:
        return {"success": True, "message": "Meeting deleted"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete meeting")
