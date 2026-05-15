from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.approvals import Approval
from app.services.notification import notification_service
from pydantic import BaseModel

router = APIRouter(prefix="/approvals", tags=["Approvals"])

class ApprovalAction(BaseModel):
    action: str
    notes: str = ""

@router.get("/")
async def list(status: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Approval)
    if status:
        query = query.where(Approval.status == status)
    result = await db.execute(query.order_by(Approval.created_at.desc()))
    return {"approvals": result.scalars().all()}

@router.get("/pending")
async def pending(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Approval).where(Approval.status == "pending").order_by(Approval.created_at.desc()))
    return {"pending": result.scalars().all()}

@router.post("/{approval_id}/action")
async def action(approval_id: int, data: ApprovalAction, db: AsyncSession = Depends(get_db)):
    approval = await db.get(Approval, approval_id)
    if not approval:
        return {"error": "Not found"}
    if data.action == "approve":
        approval.status = "approved"
        approval.approved_by = "admin"
    elif data.action == "reject":
        approval.status = "rejected"
    elif data.action == "request_changes":
        approval.status = "changes_requested"
    await db.commit()
    await notification_service.create_notification("approval_resolved", f"{approval.title}: {data.action}", "dashboard")
    return {"success": True}
