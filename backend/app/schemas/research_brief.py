from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict


class Competitor(BaseModel):
    name: str
    url: Optional[str] = None
    strength: Optional[str] = None
    weakness: Optional[str] = None


class ResearchBriefCreate(BaseModel):
    project_id: int
    summary: str
    competitors: List[Competitor]
    opportunity_score: float
    key_insights: List[str]
    raw_response: Optional[str] = None


class ResearchBriefRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    summary: str
    competitors: Any
    opportunity_score: float
    key_insights: Any
    raw_response: Optional[str] = None
    created_at: datetime
