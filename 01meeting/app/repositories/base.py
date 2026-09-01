"""Base repository class for data access."""

from typing import TypeVar, Generic, List, Optional, Type, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository for common CRUD operations."""

    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, obj_in: dict) -> T:
        """Create a new object."""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, id: int) -> Optional[T]:
        """Get object by ID."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all objects with pagination."""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def update(self, id: int, obj_in: dict) -> Optional[T]:
        """Update an object."""
        db_obj = self.get(id)
        if db_obj:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """Delete an object (hard delete)."""
        db_obj = self.get(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False

    def soft_delete(self, id: int) -> bool:
        """Soft delete an object (if model supports it)."""
        db_obj = self.get(id)
        if db_obj and hasattr(db_obj, "is_deleted"):
            db_obj.is_deleted = True
            from datetime import datetime
            if hasattr(db_obj, "deleted_at"):
                db_obj.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """Count total objects."""
        return self.db.query(self.model).count()

    def exists(self, **filters) -> bool:
        """Check if object exists with given filters."""
        return self.db.query(self.model).filter_by(**filters).first() is not None

    def filter_by(self, **filters) -> List[T]:
        """Filter objects by attributes."""
        return self.db.query(self.model).filter_by(**filters).all()

    def filter_by_one(self, **filters) -> Optional[T]:
        """Filter and return first object."""
        return self.db.query(self.model).filter_by(**filters).first()

    def order_by(self, field, descending: bool = False) -> List[T]:
        """Get all objects ordered by field."""
        order = desc(field) if descending else field
        return self.db.query(self.model).order_by(order).all()

    def order_by_paginated(
        self, field, skip: int = 0, limit: int = 100, descending: bool = False
    ) -> List[T]:
        """Get paginated objects ordered by field."""
        order = desc(field) if descending else field
        return (
            self.db.query(self.model)
            .order_by(order)
            .offset(skip)
            .limit(limit)
            .all()
        )
