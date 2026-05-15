from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.social_posts import SocialPost
from app.services.llm_manager import llm_manager
import asyncio
from datetime import datetime, timedelta

@shared_task(bind=True, max_retries=2)
def run_social_scheduler_task(self, platform, topic, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                if not job: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompt = f"Create 5 social posts for {platform} about: {topic}. Max 280 chars each. Include hashtags."
                result = await llm_manager.generate(prompt, system_prompt="Social media strategist")
                if result["success"]:
                    posts = [p.strip() for p in result["content"].split("\\n") if p.strip() and p[0].isdigit()]
                    for i, text in enumerate(posts[:5]):
                        post = SocialPost(platform=platform, content=text, scheduled_at=datetime.utcnow()+timedelta(days=i), status="scheduled")
                        db.add(post)
                    job.status = JobStatus.COMPLETED
                    job.result = {"platform": platform, "posts": len(posts[:5])}
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
