from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal, engine
from app.models.job import Job, JobStatus
from app.models.project import Project, ProjectStatus
from app.models.project_plan import ProjectPlan
from app.services.code_generator import generate_codebase
from app.services.landing_builder import generate_landing_page
import os


@shared_task(bind=True, max_retries=2)
def run_generation_task(self, project_id: int, job_id: int):
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

                # Get latest plan
                from sqlalchemy import select
                result = await db.execute(
                    select(ProjectPlan).where(ProjectPlan.project_id == project_id).order_by(ProjectPlan.created_at.desc())
                )
                plan = result.scalar_one_or_none()
                plan_data = {"tech_stack": {}, "phases": []}
                if plan:
                    plan_data = {
                        "tech_stack": plan.tech_stack or {},
                        "phases": plan.phases or [],
                        "product_name": project.name,
                        "description": project.client_idea,
                    }

                output_dir = f"/app/deliverables/project_{project_id}"

                # Generate code
                code_dir = os.path.join(output_dir, "code")
                code_files = await generate_codebase(db, project_id, project.client_idea, plan_data, code_dir)

                # Generate landing page
                landing_dir = os.path.join(output_dir, "landing")
                landing_path = await generate_landing_page(db, project_id, project.client_idea, plan_data, output_dir)

                job.status = JobStatus.COMPLETED
                job.result = {
                    "code_files": len(code_files),
                    "landing_page": landing_path,
                }
                project.status = ProjectStatus.GENERATION_REVIEW
                await db.commit()

                return {"status": "completed", "code_files": len(code_files)}

            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                project.status = ProjectStatus.FAILED
                await db.commit()
                self.retry(countdown=120, exc=e)
                return {"error": str(e)}

    return asyncio.run(_run())
