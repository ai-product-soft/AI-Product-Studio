from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.ai_call_products import AICallProduct
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_ai_call_product_task(self, config, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                if not job: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompt = "Create AI Customer Executive Call script. Natural conversation, lead qualification, appointment scheduling, objection handling, follow-up."
                result = await llm_manager.generate(prompt, system_prompt="AI voice product specialist")
                if result["success"]:
                    product = AICallProduct(name=config.get("name", "AI Sales Assistant"), description="AI-powered sales call assistant", config=config, voice_settings={"language": "en-US", "tone": "professional", "speed": "normal"}, script_template=result["content"], is_active=False)
                    db.add(product)
                    job.status = JobStatus.COMPLETED
                    job.result = {"product_id": product.id}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="ai_call_product", title="AI Call Product", description="Configuration ready", status="pending")
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
