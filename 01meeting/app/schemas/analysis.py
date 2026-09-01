from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MeetingMetadataSchema(BaseModel):
    title: str
    date: Optional[str] = None
    duration_minutes: Optional[int] = None
    participants: List[str] = []
    objective: Optional[str] = None


class KeyPointSchema(BaseModel):
    topic: str
    summary: str
    speakers: List[str] = []
    timestamps: List[str] = []
    business_impact: Optional[str] = None
    confidence: str = Field(..., pattern="^(high|medium|low)$")


class DecisionSchema(BaseModel):
    decision: str
    owner: Optional[str] = None
    rationale: Optional[str] = None
    effective_date: Optional[str] = None
    timestamp: Optional[str] = None
    confidence: str = Field(..., pattern="^(high|medium|low)$")
    evidence: Optional[str] = None


class ActionItemSchema(BaseModel):
    action_id: str
    description: str
    owner: str
    due_date: Optional[str] = None
    priority: str = Field(..., pattern="^(Critical|High|Medium|Low)$")
    status: str = Field(..., pattern="^(Open|In Progress|Blocked|Completed)$")
    dependency: Optional[str] = None
    evidence: str
    timestamp: Optional[str] = None
    confidence: str = Field(..., pattern="^(high|medium|low)$")
    commitment_type: str = Field(..., pattern="^(agreed|proposed|inferred)$")


class RiskSchema(BaseModel):
    risk_description: str
    impact: Optional[str] = None
    mitigation: Optional[str] = None
    owner: Optional[str] = None
    timestamp: Optional[str] = None
    confidence: str = Field(..., pattern="^(high|medium|low)$")
    evidence: Optional[str] = None


class IssueSchema(BaseModel):
    issue_description: str
    severity: Optional[str] = None
    owner: Optional[str] = None
    resolution: Optional[str] = None
    timestamp: Optional[str] = None
    confidence: str = Field(..., pattern="^(high|medium|low)$")
    evidence: Optional[str] = None


class OpenQuestionSchema(BaseModel):
    question: str
    asked_by: Optional[str] = None
    answer: Optional[str] = None
    timestamp: Optional[str] = None
    confidence: str = Field(..., pattern="^(high|medium|low)$")
    evidence: Optional[str] = None


class MeetingAnalysisSchema(BaseModel):
    meeting_metadata: MeetingMetadataSchema
    executive_summary: List[str] = []
    key_points: List[KeyPointSchema] = []
    decisions: List[DecisionSchema] = []
    action_items: List[ActionItemSchema] = []
    risks: List[RiskSchema] = []
    issues: List[IssueSchema] = []
    open_questions: List[OpenQuestionSchema] = []
    parking_lot: List[str] = []
    follow_ups: List[str] = []

    class Config:
        json_schema_extra = {
            "example": {
                "meeting_metadata": {
                    "title": "Q3 Planning Meeting",
                    "date": "2024-08-17",
                    "duration_minutes": 120,
                    "participants": ["Alice", "Bob"],
                    "objective": "Plan Q3 initiatives"
                },
                "executive_summary": [
                    "Team agreed on three strategic initiatives for Q3"
                ],
                "key_points": [],
                "decisions": [],
                "action_items": [],
                "risks": [],
                "issues": [],
                "open_questions": [],
                "parking_lot": [],
                "follow_ups": []
            }
        }
