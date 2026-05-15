from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.models.showcases import Showcase
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_showcaser_task(self, project_id, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompt = f"Portfolio showcase for {project.name}: {project.client_idea}. Title, description, 5 features, tech highlights, impact."
                result = await llm_manager.generate(prompt, system_prompt="Portfolio copywriter")
                if result["success"]:
                    showcase = Showcase(project_id=project_id, title=project.name, description=result["content"], tags=["AI Generated", project.status], is_featured=True)
                    db.add(showcase)
                    job.status = JobStatus.COMPLETED
                    job.result = {"showcase_id": showcase.id}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="showcaser", title=f"Portfolio: {project.name}", description="Showcase ready for website", status="pending")
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
