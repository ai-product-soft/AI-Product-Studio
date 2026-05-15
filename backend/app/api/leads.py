from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.leads import Lead
from app.models.lead_forms import LeadForm
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/leads", tags=["Leads"])

class LeadCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    source: str = "organic"
    service_interested: str

class LeadFormSubmit(BaseModel):
    business_type: str
    budget_range: str
    timeline: str
    platform: str
    description: str
    vision: str
    requirements: List[str] = []

@router.get("/")
async def list_leads(status: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Lead)
    if status:
        query = query.where(Lead.status == status)
    result = await db.execute(query.order_by(Lead.created_at.desc()))
    return {"leads": result.scalars().all()}

@router.post("/")
async def create_lead(data: LeadCreate, db: AsyncSession = Depends(get_db)):
    lead = Lead(**data.dict())
    db.add(lead)
    await db.commit()
    return {"success": True, "lead_id": lead.id}

@router.post("/{lead_id}/form")
async def submit_form(lead_id: int, data: LeadFormSubmit, db: AsyncSession = Depends(get_db)):
    form = LeadForm(lead_id=lead_id, **data.dict())
    db.add(form)
    await db.commit()
    return {"success": True, "form_id": form.id}

@router.get("/{lead_id}")
async def get_lead(lead_id: int, db: AsyncSession = Depends(get_db)):
    lead = await db.get(Lead, lead_id)
    if not lead:
        return {"error": "Lead not found"}
    result = await db.execute(select(LeadForm).where(LeadForm.lead_id == lead_id).order_by(LeadForm.created_at.desc()))
    form = result.scalar_one_or_none()
    return {"lead": lead, "form": form}
