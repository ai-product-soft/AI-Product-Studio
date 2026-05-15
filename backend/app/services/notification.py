import asyncio
from typing import Dict, Any
from app.models.notifications import Notification
from app.models.approvals import Approval
from app.db.session import AsyncSessionLocal

class NotificationService:
    WHATSAPP_ENABLED = True
    WHATSAPP_NUMBER = "+91XXXXXXXXXX"
    
    async def create_notification(self, type, message, channel="dashboard"):
        async with AsyncSessionLocal() as db:
            notif = Notification(type=type, message=message, channel=channel, status="unread")
            db.add(notif)
            await db.commit()
            if channel in ["whatsapp", "both"] and self.WHATSAPP_ENABLED:
                await self._send_whatsapp(message)
            return {"success": True, "notification_id": notif.id}
    
    async def _send_whatsapp(self, message):
        print(f"[WHATSAPP] To {self.WHATSAPP_NUMBER}: {message}")
    
    async def get_unread(self):
        async with AsyncSessionLocal() as db:
            from sqlalchemy import select
            result = await db.execute(select(Notification).where(Notification.status == "unread").order_by(Notification.created_at.desc()))
            return result.scalars().all()
    
    async def mark_read(self, notification_id):
        async with AsyncSessionLocal() as db:
            notif = await db.get(Notification, notification_id)
            if notif:
                notif.status = "read"
                await db.commit()
            return {"success": True}
    
    async def create_approval_notification(self, approval):
        message = f"Approval needed: {approval.worker_name} - {approval.title}"
        return await self.create_notification("approval_needed", message, "both")
    
    async def create_lead_notification(self, lead_name, service):
        message = f"New lead: {lead_name} - {service}"
        return await self.create_notification("new_lead", message, "both")
    
    async def create_payment_notification(self, amount, client):
        message = f"Payment: ${amount} from {client}"
        return await self.create_notification("payment_received", message, "both")
    
    async def create_proposal_notification(self, client):
        message = f"Proposal ready: {client}"
        return await self.create_notification("proposal_ready", message, "both")
    
    async def create_project_complete_notification(self, project_name):
        message = f"Project complete: {project_name}"
        return await self.create_notification("project_complete", message, "both")

notification_service = NotificationService()
