from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
from .base import Base, TimestampMixin, SoftDeleteMixin


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    teams_upn: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    teams_tenant_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_login: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    meetings: Mapped[list["Meeting"]] = relationship(
        "Meeting", back_populates="created_by", foreign_keys="Meeting.created_by_id"
    )
    processing_jobs: Mapped[list["ProcessingJob"]] = relationship(
        "ProcessingJob", back_populates="user"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog", back_populates="user"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, display_name={self.display_name})>"
