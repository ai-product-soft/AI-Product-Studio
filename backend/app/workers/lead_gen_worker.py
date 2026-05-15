from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_lead_gen_task(self, campaign_name, target_service, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                if not job: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompt = f"Create lead gen campaign: {campaign_name} for {target_service}. Headline, body, CTA, audience, 3 pain points."
                result = await llm_manager.generate(prompt, system_prompt="Lead generation specialist")
                if result["success"]:
                    job.status = JobStatus.COMPLETED
                    job.result = {"campaign": campaign_name, "content": result["content"]}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="lead_gen", title=f"Campaign: {campaign_name}", description="Lead gen campaign ready", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
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
