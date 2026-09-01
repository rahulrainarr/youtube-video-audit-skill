from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProcessingStatusSchema(BaseModel):
    job_id: str
    meeting_id: int
    status: str
    current_stage: Optional[str]
    stage_progress_percent: int
    overall_progress_percent: int
    started_at: Optional[str]
    completed_at: Optional[str]
    estimated_completion: Optional[str]
    duration_seconds: Optional[float]
    error_message: Optional[str]
    error_details: Optional[str]
    retry_count: int
    api_calls: int
    tokens_used: int
    estimated_cost: Optional[float]
    provider_used: Optional[str]
    model_used: Optional[str]

    class Config:
        from_attributes = True


class ProcessingJobSchema(BaseModel):
    id: int
    job_id: str
    meeting_id: int
    user_id: int
    status: str
    current_stage: Optional[str]
    overall_progress_percent: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
