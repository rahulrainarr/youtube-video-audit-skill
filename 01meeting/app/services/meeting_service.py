"""Meeting service for core business logic."""

import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional
import uuid

from sqlalchemy.orm import Session
from app.models import Meeting, MediaFile, User
from app.repositories import MeetingRepository, MediaFileRepository
from app.utils.file_utils import calculate_file_hash, sanitize_filename, get_file_size
from app.utils.ffmpeg_utils import extract_audio, get_audio_duration, is_ffmpeg_available
from app.core import settings

logger = logging.getLogger(__name__)


class MeetingService:
    """Service for meeting operations."""

    def __init__(self, db: Session):
        self.db = db
        self.meeting_repo = MeetingRepository(db)
        self.media_repo = MediaFileRepository(db)

    def create_meeting(
        self,
        title: str,
        user_id: int,
        description: Optional[str] = None,
        meeting_date: Optional[datetime] = None,
        location: Optional[str] = None,
        is_confidential: bool = False,
        source: str = "upload",
    ) -> Meeting:
        """Create a new meeting."""
        meeting = Meeting(
            title=title,
            description=description,
            meeting_date=meeting_date,
            location=location,
            is_confidential=is_confidential,
            created_by_id=user_id,
            source=source,
            status="pending",
        )
        self.db.add(meeting)
        self.db.commit()
        self.db.refresh(meeting)
        logger.info(f"Created meeting: {meeting.id} - {title}")
        return meeting

    def store_media_file(
        self,
        meeting_id: int,
        file_path: str,
        original_filename: str,
        file_type: str,  # 'audio', 'video', 'transcript'
        mime_type: str,
    ) -> Tuple[bool, Optional[MediaFile], str]:
        """
        Store a media file and create database record.

        Returns:
            (success, media_file, message)
        """
        try:
            # Check if meeting exists
            meeting = self.meeting_repo.get(meeting_id)
            if not meeting:
                return False, None, f"Meeting {meeting_id} not found"

            # Calculate file hash for duplicate detection
            file_hash = calculate_file_hash(file_path)

            # Check for duplicates
            existing = self.media_repo.get_by_hash(file_hash)
            if existing:
                logger.warning(f"Duplicate file detected: {existing.id}")
                return False, None, "This file has already been uploaded"

            # Get file size
            file_size = get_file_size(file_path)

            # Create database record
            media_file = MediaFile(
                meeting_id=meeting_id,
                file_name=sanitize_filename(original_filename),
                file_path=file_path,
                file_type=file_type,
                mime_type=mime_type,
                file_size_bytes=file_size,
                file_hash=file_hash,
                is_original=True,
                is_processed=False,
            )

            # Get additional metadata if audio/video
            if file_type in ["audio", "video"]:
                duration = get_audio_duration(file_path)
                if duration:
                    media_file.duration_seconds = duration

            self.db.add(media_file)
            self.db.commit()
            self.db.refresh(media_file)

            logger.info(
                f"Stored media file: {media_file.id} for meeting {meeting_id}"
            )
            return True, media_file, "File stored successfully"

        except Exception as e:
            logger.error(f"Error storing media file: {e}")
            self.db.rollback()
            return False, None, f"Error storing file: {str(e)}"

    def extract_audio_from_video(
        self,
        input_media_id: int,
        output_audio_format: str = "wav",
        sample_rate: int = 16000,
    ) -> Tuple[bool, Optional[MediaFile], str]:
        """
        Extract audio from video file.

        Returns:
            (success, audio_media_file, message)
        """
        try:
            if not is_ffmpeg_available():
                return False, None, "FFmpeg not found. Install with: choco install ffmpeg"

            # Get input media file
            input_media = self.media_repo.get(input_media_id)
            if not input_media:
                return False, None, "Input media file not found"

            if input_media.file_type != "video":
                return False, None, "Input file is not a video"

            input_path = input_media.file_path
            if not os.path.exists(input_path):
                return False, None, "Input file not found on disk"

            # Create output path
            output_dir = Path(settings.temp_dir) / "extracted_audio"
            output_dir.mkdir(parents=True, exist_ok=True)

            output_filename = f"{Path(input_path).stem}.{output_audio_format}"
            output_path = str(output_dir / output_filename)

            # Extract audio
            logger.info(f"Extracting audio from video: {input_path}")
            success, message = extract_audio(
                input_path,
                output_path,
                output_audio_format,
                sample_rate,
            )

            if not success:
                return False, None, f"Audio extraction failed: {message}"

            # Store extracted audio as new media file
            store_success, audio_media, store_msg = self.store_media_file(
                meeting_id=input_media.meeting_id,
                file_path=output_path,
                original_filename=output_filename,
                file_type="audio",
                mime_type=f"audio/{output_audio_format}",
            )

            if not store_success:
                # Clean up extracted file on failure
                try:
                    os.remove(output_path)
                except:
                    pass
                return False, None, f"Failed to store extracted audio: {store_msg}"

            # Mark as converted from the video file
            audio_media.converted_from_id = input_media_id
            self.db.commit()

            logger.info(f"Audio extracted successfully: {audio_media.id}")
            return True, audio_media, "Audio extracted successfully"

        except Exception as e:
            logger.error(f"Error extracting audio: {e}")
            return False, None, f"Error extracting audio: {str(e)}"

    def get_meeting_with_files(self, meeting_id: int) -> Optional[Meeting]:
        """Get meeting with all associated media files."""
        meeting = self.meeting_repo.get(meeting_id)
        if meeting:
            # Lazy load is automatic, but we can force load here
            if meeting.media_files:
                pass  # Force load
        return meeting

    def cleanup_temp_files(self, older_than_hours: int = 24):
        """Clean up temporary files older than specified hours."""
        try:
            import time
            temp_dir = Path(settings.temp_dir)

            if not temp_dir.exists():
                return

            current_time = time.time()
            threshold = older_than_hours * 3600

            for file_path in temp_dir.rglob("*"):
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > threshold:
                        try:
                            file_path.unlink()
                            logger.debug(f"Cleaned up temp file: {file_path}")
                        except Exception as e:
                            logger.warning(f"Failed to delete {file_path}: {e}")

        except Exception as e:
            logger.error(f"Error cleaning up temp files: {e}")

    def mark_meeting_processing(self, meeting_id: int, stage: str) -> Optional[Meeting]:
        """Update meeting status during processing."""
        return self.meeting_repo.update_status(meeting_id, f"processing_{stage}")

    def mark_meeting_completed(self, meeting_id: int) -> Optional[Meeting]:
        """Mark meeting as completed."""
        return self.meeting_repo.update_status(meeting_id, "completed")

    def mark_meeting_failed(
        self, meeting_id: int, error_message: str
    ) -> Optional[Meeting]:
        """Mark meeting as failed with error message."""
        return self.meeting_repo.update_processing_error(meeting_id, error_message)
