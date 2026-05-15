from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal, engine
from app.models.job import Job, JobStatus
from app.models.project import Project, ProjectStatus
from app.services.research_brief import generate_research_brief
from app.config import settings


@shared_task(bind=True, max_retries=3)
def run_research_task(self, project_id: int, job_id: int):
    import asyncio

    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)

                if not job or not project:
                    return {"error": "Job or project not found"}

                job.status = JobStatus.RUNNING
                await db.commit()

                brief = await generate_research_brief(db, project_id, project.client_idea)

                job.status = JobStatus.COMPLETED
                job.result = {"brief_id": brief.id, "opportunity_score": brief.opportunity_score}
                project.status = ProjectStatus.RESEARCH_COMPLETE
                await db.commit()

                return {"status": "completed", "brief_id": brief.id}

            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                project.status = ProjectStatus.FAILED
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}

    return asyncio.run(_run())
