from typing import Optional, List, Dict
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
    issue: List[AgentIssue]
    improved_text: Optional[str] = None
    verdict: str