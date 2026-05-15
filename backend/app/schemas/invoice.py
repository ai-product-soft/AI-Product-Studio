from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class InvoiceCreate(BaseModel):
    project_id: int
    amount: int
    currency: str = "usd"


class InvoiceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    stripe_payment_intent_id: Optional[str] = None
    stripe_payment_link: Optional[str] = None
    amount: int
    currency: str
    status: str
    pdf_path: Optional[str] = None
    created_at: datetime
