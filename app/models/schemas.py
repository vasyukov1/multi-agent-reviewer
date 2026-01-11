from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AdInput(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    category: Optional[str] = None
    metadata: Optional[Dict] = None


class AgentIssue(BaseModel):
    agent: str
    code: str
    message: str
    details: Optional[Dict] = None


class ReviewResult(BaseModel):
    risk_score: float = Field(..., ge=0.0, le=1.0)
    quality_score: float = Field(..., ge=0.0, le=1.0)
    issues: List[AgentIssue]
    improved_text: Optional[str] = None
    verdict: str


class PerImageScore(BaseModel):
    image_id: str
    quality_score: float = Field(..., ge=0.0, le=1.0)
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0)

    blur: float
    brightness: float
    foreground_ratio: float

    issues: List[AgentIssue]


class CVResult(BaseModel):
    cv_score: float = Field(..., ge=0.0, le=1.0)
    per_image_scores: List[PerImageScore]
    image_issues: List[AgentIssue]
    suggestions: List[str]
