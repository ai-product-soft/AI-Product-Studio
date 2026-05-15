from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.leads import Lead
from app.models.lead_forms import LeadForm
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_client_intake_task(self, lead_id, form_data):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                lead = await db.get(Lead, lead_id)
                if not lead: return {"error": "Not found"}
                form = LeadForm(lead_id=lead_id, business_type=form_data.get("business_type", "other"), budget_range=form_data.get("budget_range", "500-2k"), timeline=form_data.get("timeline", "3_months"), platform=form_data.get("platform", "web"), description=form_data.get("description", ""), vision=form_data.get("vision", ""), requirements=form_data.get("requirements", []))
                db.add(form)
                lead.form_data = form_data
                lead.status = "qualified" if form_data.get("budget_range") in ["2k-10k", "10k+"] else "contacted"
                await db.commit()
                if lead.status == "qualified":
                    await notification_service.create_lead_notification(lead.name, lead.service_interested)
                return {"lead_id": lead_id, "form_id": form.id, "status": lead.status}
            except Exception as e:
                return {"error": str(e)}
    return asyncio.run(_run())
