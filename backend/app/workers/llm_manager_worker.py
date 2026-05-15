from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.llm_settings import LLMSettings
from app.services.llm_manager import llm_manager
import asyncio

@shared_task(bind=True, max_retries=2)
def run_llm_health_check(self):
    async def _run():
        try:
            await llm_manager.load_settings()
            primary = await llm_manager.test_connection(llm_manager.settings.primary_provider, llm_manager.settings.primary_api_key, llm_manager.settings.primary_model)
            fallback1 = await llm_manager.test_connection(llm_manager.settings.fallback_1_provider, llm_manager.settings.fallback_1_api_key, llm_manager.settings.fallback_1_model)
            return {"primary": primary, "fallback_1": fallback1, "current": llm_manager.current_provider}
        except Exception as e:
            return {"error": str(e)}
    return asyncio.run(_run())
