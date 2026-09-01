from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class Experience(BaseModel):
    company: str
    position: str
    duration_years: float
    key_achievements: List[str]
    sales_metrics: Optional[Dict[str, str]] = None
    industry: Optional[str] = None


class Education(BaseModel):
    degree: str
    field: str
    institution: str


class ResumeData(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    professional_summary: str
    experiences: List[Experience]
    education: List[Education]
    certifications: List[str] = []
    skills: List[str] = []
    raw_text: str


class AnalysisMetrics(BaseModel):
    metric_name: str
    category: str  # Technical, Behavioral, Experience, etc.
    weight: float  # 0-1
    description: str
    criteria: Dict[str, str]


class ResumeAnalysis(BaseModel):
    resume_name: str
    overall_score: float
    match_percentage: float
    matched: bool  # True if >= 80%
    metric_scores: Dict[str, float]
    strengths: List[str]
    gaps: List[str]
    recommendations: List[str]
    industry_alignment: str  # High, Medium, Low
    job_readiness: str  # Ready, Developing, Needs Work


class AnalysisReport(BaseModel):
    resume_name: str
    candidate_name: str
    analysis: ResumeAnalysis
    interview_transcript: Optional[str] = None
    interview_notes: Optional[str] = None
    query_responses: Optional[Dict[str, str]] = None
    combined_assessment: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.now)
