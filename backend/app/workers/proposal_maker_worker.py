from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.proposals import Proposal
from app.models.leads import Lead
from app.models.lead_forms import LeadForm
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_proposal_maker_task(self, lead_id, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                lead = await db.get(Lead, lead_id)
                if not job or not lead: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                from sqlalchemy import select
                result = await db.execute(select(LeadForm).where(LeadForm.lead_id == lead_id).order_by(LeadForm.created_at.desc()))
                form = result.scalar_one_or_none()
                form_summary = ""
                if form:
                    form_summary = f"Business: {form.business_type}, Budget: {form.budget_range}, Timeline: {form.timeline}, Platform: {form.platform}"
                prompt = f"Create 2-3 page proposal for {lead.name}. Service: {lead.service_interested}. {form_summary}. Sections: Vision, Improvements, Workflow, Investment, Next Steps. Simple language."
                result = await llm_manager.generate(prompt, system_prompt="Professional proposal writer")
                if result["success"]:
                    proposal = Proposal(lead_id=lead_id, title=f"Proposal: {lead.name}", client_name=lead.name, vision_summary=form.vision if form else lead.service_interested, content=result["content"], status="pending_approval")
                    db.add(proposal)
                    job.status = JobStatus.COMPLETED
                    job.result = {"proposal_id": proposal.id}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="proposal_maker", title=f"Proposal: {lead.name}", description="Client proposal ready", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
                    await notification_service.create_proposal_notification(lead.name)
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
