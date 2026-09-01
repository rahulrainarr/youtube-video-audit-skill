from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MeetingCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    meeting_date: Optional[str] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    is_confidential: bool = False
    tags: Optional[List[str]] = None


class MeetingUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    meeting_date: Optional[str] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    is_confidential: Optional[bool] = None
    tags: Optional[List[str]] = None


class MeetingSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    meeting_date: Optional[str]
    duration_minutes: Optional[int]
    location: Optional[str]
    is_confidential: bool
    status: str
    source: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
