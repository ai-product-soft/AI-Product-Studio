from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import Job, JobStatus
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_self_promo_task(self, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                if not job: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()

                prompt = "Create marketing for AI Product Studio. 1 banner headline, 3 ad copies, 1 tagline."
                result = await llm_manager.generate(prompt, system_prompt="Creative copywriter")
                if result["success"]:
                    job.status = JobStatus.COMPLETED
                    job.result = {"content": result["content"]}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="self_promo", title="Self-Promo Ready", description="Review banner/ad content", status="pending")
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
