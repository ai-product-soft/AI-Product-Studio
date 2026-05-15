from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_service_promo_task(self, service_type, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                if not job: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                services = {"sem": "Search Engine Marketing", "website": "Website Build", "design": "UI/UX Design", "landing": "Landing Pages", "full_marketing": "Full Digital Marketing"}
                desc = services.get(service_type, "Digital Marketing")
                prompt = f"Create marketing for: {desc}. Headline, 3 benefits, CTA, 2 social ads."
                result = await llm_manager.generate(prompt, system_prompt="Marketing specialist")
                if result["success"]:
                    job.status = JobStatus.COMPLETED
                    job.result = {"service": service_type, "content": result["content"]}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="service_promo", title=f"{service_type.upper()} Promo", description="Service promotion ready", status="pending")
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
