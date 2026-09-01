from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Enum,
    ForeignKey, Float, JSON, Index
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from enum import Enum as PyEnum
from datetime import datetime
from typing import Optional, List
from .base import Base, TimestampMixin, SoftDeleteMixin


class MeetingSourceEnum(PyEnum):
    UPLOAD = "upload"
    TEAMS_VTT = "teams_vtt"
    TEAMS_DOCX = "teams_docx"
    TEAMS_TRANSCRIPT = "teams_transcript"
    TEAMS_GRAPH = "teams_graph"
    MICROPHONE = "microphone"
    OTHER = "other"


class MeetingStatusEnum(PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    TRANSCRIBING = "transcribing"
    DIARIZING = "diarizing"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


class Meeting(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "meetings"
    __table_args__ = (
        Index("idx_created_by_id", "created_by_id"),
        Index("idx_meeting_date", "meeting_date"),
        Index("idx_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    meeting_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    meeting_start_time: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    status: Mapped[str] = mapped_column(
        Enum(MeetingStatusEnum),
        default=MeetingStatusEnum.PENDING,
        nullable=False,
        index=True
    )
    source: Mapped[str] = mapped_column(
        Enum(MeetingSourceEnum),
        default=MeetingSourceEnum.UPLOAD,
        nullable=False
    )

    created_by_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    # Microsoft Teams specific
    teams_meeting_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    teams_event_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    teams_channel_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Metadata
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_confidential: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON-encoded list

    # Processing metadata
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    processing_duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    transcription_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    created_by: Mapped["User"] = relationship(
        "User", back_populates="meetings", foreign_keys=[created_by_id]
    )
    participants: Mapped[List["Participant"]] = relationship(
        "Participant", back_populates="meeting", cascade="all, delete-orphan"
    )
    media_files: Mapped[List["MediaFile"]] = relationship(
        "MediaFile", back_populates="meeting", cascade="all, delete-orphan"
    )
    transcript: Mapped[Optional["Transcript"]] = relationship(
        "Transcript", back_populates="meeting", uselist=False, cascade="all, delete-orphan"
    )
    summaries: Mapped[List["Summary"]] = relationship(
        "Summary", back_populates="meeting", cascade="all, delete-orphan"
    )
    key_points: Mapped[List["KeyPoint"]] = relationship(
        "KeyPoint", back_populates="meeting", cascade="all, delete-orphan"
    )
    decisions: Mapped[List["Decision"]] = relationship(
        "Decision", back_populates="meeting", cascade="all, delete-orphan"
    )
    action_items: Mapped[List["ActionItem"]] = relationship(
        "ActionItem", back_populates="meeting", cascade="all, delete-orphan"
    )
    risks: Mapped[List["Risk"]] = relationship(
        "Risk", back_populates="meeting", cascade="all, delete-orphan"
    )
    issues: Mapped[List["Issue"]] = relationship(
        "Issue", back_populates="meeting", cascade="all, delete-orphan"
    )
    open_questions: Mapped[List["OpenQuestion"]] = relationship(
        "OpenQuestion", back_populates="meeting", cascade="all, delete-orphan"
    )
    export_records: Mapped[List["ExportRecord"]] = relationship(
        "ExportRecord", back_populates="meeting", cascade="all, delete-orphan"
    )
    processing_jobs: Mapped[List["ProcessingJob"]] = relationship(
        "ProcessingJob", back_populates="meeting", cascade="all, delete-orphan"
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog", back_populates="meeting", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Meeting(id={self.id}, title={self.title}, status={self.status})>"
