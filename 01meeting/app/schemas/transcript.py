from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TranscriptSegmentSchema(BaseModel):
    id: int
    segment_index: int
    start_time: float
    end_time: float
    speaker_label: Optional[str]
    speaker_name: Optional[str]
    text: str
    edited_text: Optional[str]
    confidence: Optional[float]
    is_edited: bool
    is_uncertain: bool
    word_count: int

    class Config:
        from_attributes = True


class TranscriptSchema(BaseModel):
    id: int
    meeting_id: int
    raw_transcript: str
    edited_transcript: Optional[str]
    language: str
    is_translated: bool
    transcription_provider: str
    transcription_model: str
    average_confidence: Optional[float]
    has_speaker_diarization: bool
    diarization_model: Optional[str]
    is_edited: bool
    edit_count: int
    requires_review: bool
    word_count: int
    unique_speakers: int
    segments: List[TranscriptSegmentSchema] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
