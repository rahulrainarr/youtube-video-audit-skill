from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
from .base import Base, TimestampMixin


class Participant(Base, TimestampMixin):
    __tablename__ = "participants"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
        Index("idx_email", "email"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    role: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    speaker_label: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_organizer: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    teams_upn: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    meeting: Mapped["Meeting"] = relationship(
        "Meeting", back_populates="participants"
    )

    def __repr__(self):
        return f"<Participant(id={self.id}, name={self.name}, email={self.email})>"
