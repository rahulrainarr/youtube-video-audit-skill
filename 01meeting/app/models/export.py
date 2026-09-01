from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Index, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from enum import Enum as PyEnum
from typing import Optional
from .base import Base, TimestampMixin, SoftDeleteMixin


class ExportFormatEnum(PyEnum):
    DOCX = "docx"
    PDF = "pdf"
    MARKDOWN = "markdown"
    JSON = "json"
    CSV = "csv"
    VTT = "vtt"
    SRT = "srt"
    PLAINTEXT = "plaintext"


class ExportRecord(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "export_records"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False
    )

    export_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    format: Mapped[str] = mapped_column(Enum(ExportFormatEnum), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    export_type: Mapped[str] = mapped_column(String(100), nullable=False)  # summary, full_report, transcript, actions

    # Metadata
    includes_original_transcript: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    includes_edited_transcript: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    includes_summary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    includes_actions: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    includes_risks: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    includes_decisions: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="export_records")

    def __repr__(self):
        return f"<ExportRecord(id={self.export_id}, format={self.format})>"
