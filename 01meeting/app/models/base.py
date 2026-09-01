from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.orm import declarative_base, MappedColumn
from typing import Optional

Base = declarative_base()


class TimestampMixin:
    """Mixin providing created and updated timestamps."""

    created_at: MappedColumn[datetime] = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: MappedColumn[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class SoftDeleteMixin:
    """Mixin providing soft-delete capability."""

    is_deleted: MappedColumn[bool] = Column(Boolean, default=False, nullable=False)
    deleted_at: MappedColumn[Optional[datetime]] = Column(DateTime, nullable=True)
