from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Boolean, Index, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List
from .base import Base, TimestampMixin


class Transcript(Base, TimestampMixin):
    __tablename__ = "transcripts"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False, unique=True
    )

    # Content versions
    raw_transcript: Mapped[Text] = mapped_column(Text, nullable=False)
    edited_transcript: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    is_translated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Transcription metadata
    transcription_provider: Mapped[str] = mapped_column(String(50), nullable=False)
    transcription_model: Mapped[str] = mapped_column(String(100), nullable=False)
    average_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    has_speaker_diarization: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    diarization_model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Processing flags
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    edit_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    requires_review: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Word count and metrics
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unique_speakers: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="transcript")
    segments: Mapped[List["TranscriptSegment"]] = relationship(
        "TranscriptSegment", back_populates="transcript", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Transcript(id={self.id}, meeting_id={self.meeting_id}, language={self.language})>"


class TranscriptSegment(Base, TimestampMixin):
    __tablename__ = "transcript_segments"
    __table_args__ = (
        Index("idx_transcript_id", "transcript_id"),
        Index("idx_start_time", "start_time"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transcript_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("transcripts.id"), nullable=False
    )

    # Timing
    segment_index: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[float] = mapped_column(Float, nullable=False)
    end_time: Mapped[float] = mapped_column(Float, nullable=False)

    # Speaker information
    speaker_label: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    speaker_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Content
    text: Mapped[str] = mapped_column(Text, nullable=False)
    edited_text: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)

    # Quality metrics
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_uncertain: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Metadata
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    transcript: Mapped["Transcript"] = relationship(
        "Transcript", back_populates="segments"
    )

    def __repr__(self):
        return f"<TranscriptSegment(id={self.id}, speaker={self.speaker_label}, start={self.start_time})>"
