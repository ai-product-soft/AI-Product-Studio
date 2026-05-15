from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict


class AdCampaignCreate(BaseModel):
    project_id: int
    platform: str
    ad_copy: Any


class AdCampaignRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    platform: str
    ad_copy: Any
    status: str
    created_at: datetime
