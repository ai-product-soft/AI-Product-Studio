from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_website_builder_task(self, project_id, website_type, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                types = {"portfolio": "Portfolio", "ecommerce": "E-commerce", "saas": "SaaS", "business": "Business", "landing": "Landing page"}
                desc = types.get(website_type, "Custom")
                prompt = f"Website spec for {desc}: {project.name}. Site structure, sections, design system, interactive elements, responsive, SEO."
                result = await llm_manager.generate(prompt, system_prompt="Senior web developer", max_tokens=4000)
                if result["success"]:
                    job.status = JobStatus.COMPLETED
                    job.result = {"type": website_type, "spec": result["content"]}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="website_builder", title=f"Website: {project.name}", description=f"{desc} spec ready", status="pending")
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
