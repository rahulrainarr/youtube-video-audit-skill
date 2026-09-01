from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
from .base import Base, TimestampMixin, SoftDeleteMixin


class MediaFile(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "media_files"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
        Index("idx_file_hash", "file_hash"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False
    )

    file_name: Mapped[str] = mapped_column(String(500), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)  # audio, video, transcript
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    file_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    # Media properties
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sample_rate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    channels: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    codec: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    is_original: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    converted_from_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("media_files.id"), nullable=True
    )

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="media_files")
    converted_files: Mapped[list["MediaFile"]] = relationship(
        "MediaFile",
        remote_side=[id],
        backref="converted_from",
        foreign_keys=[converted_from_id]
    )

    def __repr__(self):
        return f"<MediaFile(id={self.id}, file_name={self.file_name}, file_type={self.file_type})>"
