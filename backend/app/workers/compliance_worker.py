from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.models.compliance_docs import ComplianceDoc
from app.services.llm_manager import llm_manager
import asyncio

@shared_task(bind=True, max_retries=2)
def run_compliance_task(self, project_id, doc_type, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompts = {"manual": f"User manual for {project.name}", "privacy_policy": f"Privacy policy for {project.name}", "terms_conditions": f"T&C for {project.name}", "guidelines": f"Usage guidelines for {project.name}", "rules": f"Business rules for {project.name}"}
                prompt = prompts.get(doc_type, f"Documentation for {project.name}")
                result = await llm_manager.generate(prompt, system_prompt="Legal documentation specialist")
                if result["success"]:
                    doc = ComplianceDoc(project_id=project_id, doc_type=doc_type, title=f"{doc_type.replace('_', ' ').title()}: {project.name}", content=result["content"])
                    db.add(doc)
                    job.status = JobStatus.COMPLETED
                    job.result = {"doc_id": doc.id, "type": doc_type}
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
