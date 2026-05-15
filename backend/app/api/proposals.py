from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.proposals import Proposal
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/proposals", tags=["Proposals"])

class ProposalUpdate(BaseModel):
    status: Optional[str] = None
    content: Optional[str] = None

@router.get("/")
async def list_proposals(status: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Proposal)
    if status:
        query = query.where(Proposal.status == status)
    result = await db.execute(query.order_by(Proposal.created_at.desc()))
    return {"proposals": result.scalars().all()}

@router.get("/{proposal_id}")
async def get_proposal(proposal_id: int, db: AsyncSession = Depends(get_db)):
    proposal = await db.get(Proposal, proposal_id)
    if not proposal:
        return {"error": "Proposal not found"}
    return {"proposal": proposal}

@router.post("/{proposal_id}/update")
async def update_proposal(proposal_id: int, data: ProposalUpdate, db: AsyncSession = Depends(get_db)):
    proposal = await db.get(Proposal, proposal_id)
    if not proposal:
        return {"error": "Proposal not found"}
    if data.status:
        proposal.status = data.status
    if data.content:
        proposal.content = data.content
    await db.commit()
    return {"success": True, "proposal": proposal}
