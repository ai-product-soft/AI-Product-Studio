from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.notifications import Notification
from app.services.notification import notification_service
from pydantic import BaseModel

router = APIRouter(prefix="/notifications", tags=["Notifications"])

class Settings(BaseModel):
    whatsapp_number: str
    enable_whatsapp: bool = True
    enable_dashboard: bool = True

@router.get("/")
async def get(limit: int = 50, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Notification).order_by(Notification.created_at.desc()).limit(limit))
    return {"notifications": result.scalars().all()}

@router.get("/unread")
async def unread(db: AsyncSession = Depends(get_db)):
    return {"unread": await notification_service.get_unread()}

@router.post("/{notification_id}/read")
async def mark_read(notification_id: int):
    return await notification_service.mark_read(notification_id)

@router.post("/settings")
async def update_settings(data: Settings):
    notification_service.WHATSAPP_NUMBER = data.whatsapp_number
    notification_service.WHATSAPP_ENABLED = data.enable_whatsapp
    return {"success": True}
