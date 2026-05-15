from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.session import engine
from app.models.job import Job, JobStatus
from app.models.project import Project, ProjectStatus
from app.models.project_plan import ProjectPlan
from app.services.ad_creative_generator import generate_ad_creatives
from app.services.content_generator import generate_content
import os


@shared_task(bind=True, max_retries=2)
def run_promotion_task(self, project_id: int, job_id: int):
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

                from sqlalchemy import select
                result = await db.execute(
                    select(ProjectPlan).where(ProjectPlan.project_id == project_id).order_by(ProjectPlan.created_at.desc())
                )
                plan = result.scalar_one_or_none()
                plan_data = {"features": []}
                if plan and plan.tech_stack:
                    plan_data = plan.tech_stack
                    plan_data["features"] = [p.get("phase", "") for p in (plan.phases or [])]

                output_dir = f"/app/deliverables/project_{project_id}"

                # Generate ad creatives
                campaigns = await generate_ad_creatives(db, project_id, project.client_idea, plan_data)

                # Generate content
                content = await generate_content(db, project_id, project.client_idea, plan_data, output_dir)

                job.status = JobStatus.COMPLETED
                job.result = {
                    "campaigns": list(campaigns.keys()),
                    "content": content,
                }
                project.status = ProjectStatus.SALES_READY
                await db.commit()

                return {"status": "completed", "campaigns": list(campaigns.keys())}

            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                project.status = ProjectStatus.FAILED
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}

    return asyncio.run(_run())
