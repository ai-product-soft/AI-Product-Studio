from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal, engine
from app.models.job import Job, JobStatus
from app.models.project import Project, ProjectStatus
from app.services.ad_creative_generator import generate_ad_creatives
from app.services.content_generator import generate_blog_post, generate_social_posts


@shared_task(bind=True, max_retries=2)
def run_promotion_task(self, project_id: int, job_id: int):
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

                # Generate ad creatives
                ad_creatives = await generate_ad_creatives(db, project_id, project.name, project.client_idea)

                # Generate blog post
                blog_post = await generate_blog_post(db, project_id, project.name, project.client_idea)

                # Generate social posts
                social_posts = await generate_social_posts(db, project_id, project.name, project.client_idea)

                job.status = JobStatus.COMPLETED
                job.result = {
                    "ad_creatives": len(ad_creatives),
                    "blog_post": blog_post,
                    "social_posts": len(social_posts),
                }
                project.status = ProjectStatus.PROMOTION_REVIEW
                await db.commit()

                return {"status": "completed", "ads": len(ad_creatives), "social": len(social_posts)}

            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                project.status = ProjectStatus.FAILED
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}

    return asyncio.run(_run())
