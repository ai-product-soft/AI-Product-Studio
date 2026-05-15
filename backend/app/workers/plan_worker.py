from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.session import engine
from app.models.job import Job, JobStatus
from app.models.project import Project, ProjectStatus
from app.models.research_brief import ResearchBrief
from app.services.project_plan import generate_project_plan


@shared_task(bind=True, max_retries=3)
def run_plan_task(self, project_id: int, job_id: int):
    import asyncio

    async def _run():
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)

                if not job or not project:
                    return {"error": "Job or project not found"}

                job.status = JobStatus.RUNNING
                await db.commit()

                # Get latest research brief
                from sqlalchemy import select
                result = await db.execute(
                    select(ResearchBrief).where(ResearchBrief.project_id == project_id).order_by(ResearchBrief.created_at.desc())
                )
                brief = result.scalar_one_or_none()
                research_summary = brief.summary if brief else "No research available"

                plan = await generate_project_plan(db, project_id, project.client_idea, research_summary)

                job.status = JobStatus.COMPLETED
                job.result = {"plan_id": plan.id}
                project.status = ProjectStatus.PLAN_COMPLETE
                await db.commit()

                return {"status": "completed", "plan_id": plan.id}

            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                project.status = ProjectStatus.FAILED
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}

    return asyncio.run(_run())
