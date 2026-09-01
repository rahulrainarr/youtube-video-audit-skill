from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Enum, Index, JSON, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from enum import Enum as PyEnum
from typing import Optional
from .base import Base, TimestampMixin


class ConfidenceEnum(PyEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PriorityEnum(PyEnum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class ActionStatusEnum(PyEnum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"
    COMPLETED = "Completed"


class CommitmentTypeEnum(PyEnum):
    AGREED = "agreed"
    PROPOSED = "proposed"
    INFERRED = "inferred"


class Summary(Base, TimestampMixin):
    __tablename__ = "summaries"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False
    )

    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    bullet_points: Mapped[str] = mapped_column(Text, nullable=False)  # JSON-encoded list
    generated_by: Mapped[str] = mapped_column(String(100), nullable=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="summaries")

    def __repr__(self):
        return f"<Summary(id={self.id}, meeting_id={self.meeting_id})>"


class KeyPoint(Base, TimestampMixin):
    __tablename__ = "key_points"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False
    )

    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    speakers: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON-encoded list
    timestamps: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON-encoded list
    business_impact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[str] = mapped_column(
        Enum(ConfidenceEnum), default=ConfidenceEnum.MEDIUM, nullable=False
    )
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="key_points")

    def __repr__(self):
        return f"<KeyPoint(id={self.id}, topic={self.topic})>"


class Decision(Base, TimestampMixin):
    __tablename__ = "decisions"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False
    )

    decision: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    effective_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    timestamp: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence: Mapped[str] = mapped_column(
        Enum(ConfidenceEnum), default=ConfidenceEnum.MEDIUM, nullable=False
    )
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="decisions")

    def __repr__(self):
        return f"<Decision(id={self.id}, owner={self.owner})>"


class ActionItem(Base, TimestampMixin):
    __tablename__ = "action_items"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
        Index("idx_owner", "owner"),
        Index("idx_priority", "priority"),
        Index("idx_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False
    )

    action_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    due_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    priority: Mapped[str] = mapped_column(
        Enum(PriorityEnum), default=PriorityEnum.MEDIUM, nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        Enum(ActionStatusEnum), default=ActionStatusEnum.OPEN, nullable=False, index=True
    )
    dependency: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    evidence: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence: Mapped[str] = mapped_column(
        Enum(ConfidenceEnum), default=ConfidenceEnum.MEDIUM, nullable=False
    )
    commitment_type: Mapped[str] = mapped_column(
        Enum(CommitmentTypeEnum), default=CommitmentTypeEnum.AGREED, nullable=False
    )
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="action_items")

    def __repr__(self):
        return f"<ActionItem(id={self.action_id}, owner={self.owner}, status={self.status})>"


class Risk(Base, TimestampMixin):
    __tablename__ = "risks"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False
    )

    risk_description: Mapped[str] = mapped_column(Text, nullable=False)
    impact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mitigation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence: Mapped[str] = mapped_column(
        Enum(ConfidenceEnum), default=ConfidenceEnum.MEDIUM, nullable=False
    )
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="risks")

    def __repr__(self):
        return f"<Risk(id={self.id}, meeting_id={self.meeting_id})>"


class Issue(Base, TimestampMixin):
    __tablename__ = "issues"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False
    )

    issue_description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence: Mapped[str] = mapped_column(
        Enum(ConfidenceEnum), default=ConfidenceEnum.MEDIUM, nullable=False
    )
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="issues")

    def __repr__(self):
        return f"<Issue(id={self.id}, meeting_id={self.meeting_id})>"


class OpenQuestion(Base, TimestampMixin):
    __tablename__ = "open_questions"
    __table_args__ = (
        Index("idx_meeting_id", "meeting_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("meetings.id"), nullable=False
    )

    question: Mapped[str] = mapped_column(Text, nullable=False)
    asked_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence: Mapped[str] = mapped_column(
        Enum(ConfidenceEnum), default=ConfidenceEnum.MEDIUM, nullable=False
    )
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="open_questions")

    def __repr__(self):
        return f"<OpenQuestion(id={self.id}, meeting_id={self.meeting_id})>"
