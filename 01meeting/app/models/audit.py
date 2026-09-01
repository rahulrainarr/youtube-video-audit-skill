from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
from .base import Base, TimestampMixin


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_meeting_id", "meeting_id"),
        Index("idx_action", "action"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    meeting_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=True
    )

    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    change_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON

    # Context
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="audit_logs")
    meeting: Mapped[Optional["Meeting"]] = relationship("Meeting", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, entity_type={self.entity_type})>"
