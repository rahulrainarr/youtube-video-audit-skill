"""Repository for Meeting model."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime
from app.models import Meeting, MediaFile
from .base import BaseRepository


class MeetingRepository(BaseRepository[Meeting]):
    """Repository for Meeting model."""

    def __init__(self, db: Session):
        super().__init__(db, Meeting)

    def get_by_title(self, title: str) -> Optional[Meeting]:
        """Get meeting by title."""
        return self.filter_by_one(title=title)

    def get_user_meetings(self, user_id: int, skip: int = 0, limit: int = 50) -> List[Meeting]:
        """Get all meetings for a user."""
        return (
            self.db.query(self.model)
            .filter(self.model.created_by_id == user_id)
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_user_meetings(self, user_id: int) -> int:
        """Count meetings for a user."""
        return self.db.query(self.model).filter(
            self.model.created_by_id == user_id
        ).count()

    def get_by_status(self, status: str) -> List[Meeting]:
        """Get meetings by status."""
        return self.filter_by(status=status)

    def get_by_source(self, source: str) -> List[Meeting]:
        """Get meetings by source."""
        return self.filter_by(source=source)

    def get_pending_processing(self) -> List[Meeting]:
        """Get meetings pending processing."""
        return self.db.query(self.model).filter(
            self.model.status.in_(["pending", "processing"])
        ).all()

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Meeting]:
        """Get meetings within a date range."""
        return self.db.query(self.model).filter(
            and_(
                self.model.meeting_date >= start_date,
                self.model.meeting_date <= end_date,
            )
        ).all()

    def search_by_title(self, search_term: str) -> List[Meeting]:
        """Search meetings by title."""
        return self.db.query(self.model).filter(
            self.model.title.ilike(f"%{search_term}%")
        ).all()

    def get_recent(self, limit: int = 10) -> List[Meeting]:
        """Get most recent meetings."""
        return (
            self.db.query(self.model)
            .order_by(desc(self.model.created_at))
            .limit(limit)
            .all()
        )

    def get_total_duration(self, user_id: int) -> int:
        """Get total meeting duration for a user in minutes."""
        from sqlalchemy import func
        result = self.db.query(func.sum(self.model.duration_minutes)).filter(
            self.model.created_by_id == user_id
        ).scalar()
        return result or 0

    def get_with_media_files(self, meeting_id: int) -> Optional[Meeting]:
        """Get meeting with its media files."""
        return (
            self.db.query(self.model)
            .filter(self.model.id == meeting_id)
            .first()
        )

    def update_status(self, meeting_id: int, status: str) -> Optional[Meeting]:
        """Update meeting status."""
        meeting = self.get(meeting_id)
        if meeting:
            meeting.status = status
            self.db.commit()
            self.db.refresh(meeting)
        return meeting

    def update_processing_error(
        self, meeting_id: int, error_message: str
    ) -> Optional[Meeting]:
        """Update meeting with processing error."""
        meeting = self.get(meeting_id)
        if meeting:
            meeting.status = "failed"
            meeting.error_message = error_message
            self.db.commit()
            self.db.refresh(meeting)
        return meeting

    def get_confidential(self, user_id: int) -> List[Meeting]:
        """Get confidential meetings for a user."""
        return self.db.query(self.model).filter(
            and_(
                self.model.created_by_id == user_id,
                self.model.is_confidential == True,
            )
        ).all()
