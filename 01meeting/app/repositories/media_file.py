"""Repository for MediaFile model."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import MediaFile
from .base import BaseRepository


class MediaFileRepository(BaseRepository[MediaFile]):
    """Repository for MediaFile model."""

    def __init__(self, db: Session):
        super().__init__(db, MediaFile)

    def get_by_meeting(self, meeting_id: int) -> List[MediaFile]:
        """Get all media files for a meeting."""
        return self.filter_by(meeting_id=meeting_id)

    def get_original_files(self, meeting_id: int) -> List[MediaFile]:
        """Get original uploaded files for a meeting."""
        return self.db.query(self.model).filter(
            and_(
                self.model.meeting_id == meeting_id,
                self.model.is_original == True,
            )
        ).all()

    def get_by_hash(self, file_hash: str) -> Optional[MediaFile]:
        """Get file by hash (detect duplicates)."""
        return self.filter_by_one(file_hash=file_hash)

    def get_by_type(self, meeting_id: int, file_type: str) -> List[MediaFile]:
        """Get files by type (audio, video, transcript)."""
        return self.db.query(self.model).filter(
            and_(
                self.model.meeting_id == meeting_id,
                self.model.file_type == file_type,
            )
        ).all()

    def get_processed_files(self, meeting_id: int) -> List[MediaFile]:
        """Get processed files for a meeting."""
        return self.db.query(self.model).filter(
            and_(
                self.model.meeting_id == meeting_id,
                self.model.is_processed == True,
            )
        ).all()

    def get_unprocessed_files(self, meeting_id: int) -> List[MediaFile]:
        """Get unprocessed files for a meeting."""
        return self.db.query(self.model).filter(
            and_(
                self.model.meeting_id == meeting_id,
                self.model.is_processed == False,
            )
        ).all()

    def update_as_processed(self, file_id: int) -> Optional[MediaFile]:
        """Mark a file as processed."""
        file = self.get(file_id)
        if file:
            file.is_processed = True
            self.db.commit()
            self.db.refresh(file)
        return file

    def get_by_name(self, meeting_id: int, file_name: str) -> Optional[MediaFile]:
        """Get file by name for a meeting."""
        return self.filter_by_one(meeting_id=meeting_id, file_name=file_name)

    def get_total_size(self, meeting_id: int) -> int:
        """Get total file size for a meeting in bytes."""
        from sqlalchemy import func
        result = self.db.query(func.sum(self.model.file_size_bytes)).filter(
            self.model.meeting_id == meeting_id
        ).scalar()
        return result or 0

    def has_converted_files(self, media_file_id: int) -> bool:
        """Check if a file has converted versions."""
        return self.exists(converted_from_id=media_file_id)

    def get_converted_files(self, original_file_id: int) -> List[MediaFile]:
        """Get all converted versions of a file."""
        return self.filter_by(converted_from_id=original_file_id)
