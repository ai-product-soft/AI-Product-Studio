from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.models.documents import Document
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_documentor_task(self, project_id, doc_type, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                types = {"prd": "Product Requirements", "trd": "Technical Requirements", "ui_ux": "UI/UX Design", "appflows": "Application Flows", "backend_schema": "Backend Schema", "implementation_plan": "Implementation Plan"}
                name = types.get(doc_type, "Technical Document")
                prompt = f"Create {name} for {project.name}: {project.client_idea}. Comprehensive specs, diagrams, data models, API contracts, phases. INTERNAL."
                result = await llm_manager.generate(prompt, system_prompt="Technical documentation specialist", max_tokens=4000)
                if result["success"]:
                    doc = Document(project_id=project_id, doc_type=doc_type, title=f"{name}: {project.name}", content=result["content"], status="draft")
                    db.add(doc)
                    job.status = JobStatus.COMPLETED
                    job.result = {"doc_id": doc.id, "type": doc_type}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="documentor", title=f"{name}: {project.name}", description=f"{name} ready (INTERNAL)", status="pending")
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
