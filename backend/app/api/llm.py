from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.llm_settings import LLMSettings
from app.services.llm_manager import llm_manager
from pydantic import BaseModel

router = APIRouter(prefix="/llm", tags=["LLM"])

class LLMSettingsUpdate(BaseModel):
    primary_provider: str = "google"
    primary_model: str = "gemini-2.5-flash"
    primary_api_key: str = ""
    fallback_1_provider: str = "groq"
    fallback_1_model: str = "llama-3.3-70b"
    fallback_1_api_key: str = ""
    fallback_2_provider: str = "cerebras"
    fallback_2_model: str = "llama-3.3-70b"
    fallback_2_api_key: str = ""
    fallback_3_provider: str = "openrouter"
    fallback_3_model: str = "auto"
    fallback_3_api_key: str = ""
    local_model: str = "gemma3:4b"
    ollama_url: str = "http://ollama:11434"
    auto_switch: bool = True
    timeout_seconds: int = 30

@router.get("/settings")
async def get_settings(db: AsyncSession = Depends(get_db)):
    settings = await db.get(LLMSettings, 1)
    if not settings:
        settings = LLMSettings()
        db.add(settings)
        await db.commit()
    return settings

@router.post("/settings")
async def update_settings(data: LLMSettingsUpdate, db: AsyncSession = Depends(get_db)):
    settings = await db.get(LLMSettings, 1)
    if not settings:
        settings = LLMSettings(**data.dict())
        db.add(settings)
    else:
        for k, v in data.dict().items():
            setattr(settings, k, v)
    await db.commit()
    return {"success": True}

@router.post("/test/{provider}")
async def test(provider: str, api_key: str, model: str):
    return await llm_manager.test_connection(provider, api_key, model)

@router.get("/status")
async def status():
    return {"current_provider": llm_manager.current_provider, "current_model": llm_manager.current_model}
