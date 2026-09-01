from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Float, Boolean, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from enum import Enum as PyEnum
from typing import Optional
from .base import Base, TimestampMixin


class ProcessingStatusEnum(PyEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProcessingStageEnum(PyEnum):
    VALIDATION = "validation"
    MEDIA_EXTRACTION = "media_extraction"
    TRANSCRIPTION = "transcription"
    DIARIZATION = "diarization"
    ANALYSIS = "analysis"
    EXPORT = "export"


class ProcessingJob(Base, TimestampMixin):
    __tablename__ = "processing_jobs"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
        Index("idx_user_id", "user_id"),
        Index("idx_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    status: Mapped[str] = mapped_column(
        Enum(ProcessingStatusEnum),
        default=ProcessingStatusEnum.PENDING,
        nullable=False,
        index=True
    )
    current_stage: Mapped[Optional[str]] = mapped_column(
        Enum(ProcessingStageEnum), nullable=True
    )
    stage_progress_percent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    overall_progress_percent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Timing
    started_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    completed_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    estimated_completion: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Error handling
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=3, nullable=False)

    # Cost tracking
    api_calls: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    tokens_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estimated_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Processing parameters
    provider_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="processing_jobs")
    user: Mapped["User"] = relationship("User", back_populates="processing_jobs")

    def __repr__(self):
        return f"<ProcessingJob(id={self.job_id}, status={self.status}, progress={self.overall_progress_percent}%)>"
