from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.notifications import Notification
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_notification_sender(self, notification_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                notif = await db.get(Notification, notification_id)
                if not notif: return {"error": "Not found"}
                if notif.channel in ["whatsapp", "both"]:
                    await notification_service._send_whatsapp(notif.message)
                notif.status = "sent"
                await db.commit()
                return {"status": "sent", "id": notification_id}
            except Exception as e:
                return {"error": str(e)}
    return asyncio.run(_run())
