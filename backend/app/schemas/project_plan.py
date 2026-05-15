from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict


class ProjectPlanCreate(BaseModel):
    project_id: int
    phases: Any
    tech_stack: Any
    monetization_strategy: Optional[str] = None


class ProjectPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    phases: Any
    tech_stack: Any
    monetization_strategy: Optional[str] = None
    created_at: datetime
