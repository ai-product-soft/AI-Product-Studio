from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.leads import Lead
import asyncio

@shared_task(bind=True, max_retries=2)
def run_lead_manager_task(self, lead_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                lead = await db.get(Lead, lead_id)
                if not lead: return {"error": "Not found"}
                score = 0
                if lead.company: score += 20
                if lead.budget_range and lead.budget_range != "500-2k": score += 30
                if lead.service_interested in ["full_marketing", "product_studio"]: score += 25
                if lead.source in ["meta_ads", "google_ads"]: score += 15
                lead.score = min(score, 100)
                if lead.score >= 70: lead.status = "qualified"
                elif lead.score >= 40: lead.status = "contacted"
                await db.commit()
                return {"lead_id": lead_id, "score": lead.score, "status": lead.status}
            except Exception as e:
                return {"error": str(e)}
    return asyncio.run(_run())
