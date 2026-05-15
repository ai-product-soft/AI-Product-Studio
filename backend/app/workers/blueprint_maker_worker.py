from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.models.blueprints import Blueprint
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_blueprint_maker_task(self, project_id, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompt = f"Technical blueprint for {project.name}: {project.client_idea}. Tech stack, architecture, DB schema, API design, security, deployment. INTERNAL ONLY."
                result = await llm_manager.generate(prompt, system_prompt="Senior software architect", max_tokens=4000)
                if result["success"]:
                    blueprint = Blueprint(project_id=project_id, title=f"Blueprint: {project.name}", tech_stack={}, architecture=result["content"], is_internal=True)
                    db.add(blueprint)
                    job.status = JobStatus.COMPLETED
                    job.result = {"blueprint_id": blueprint.id}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="blueprint_maker", title=f"Blueprint: {project.name}", description="Technical blueprint ready (INTERNAL)", status="pending")
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
