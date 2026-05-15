from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    project_id: int
    job_type: str


class JobCreate(JobBase):
    pass


class JobRead(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    celery_task_id: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
