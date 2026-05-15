import asyncio
import httpx
import redis.asyncio as redis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import get_db
from app.config import settings

router = APIRouter(prefix="/health", tags=["health"])


async def check_db(db: AsyncSession) -> dict:
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "service": "database"}
    except Exception as e:
        return {"status": "error", "service": "database", "detail": str(e)}


async def check_redis() -> dict:
    try:
        r = redis.from_url(settings.REDIS_URL, socket_connect_timeout=5)
        await r.ping()
        await r.close()
        return {"status": "ok", "service": "redis"}
    except Exception as e:
        return {"status": "error", "service": "redis", "detail": str(e)}


async def check_ollama() -> dict:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{settings.OLLAMA_URL}/api/tags")
            resp.raise_for_status()
            return {"status": "ok", "service": "ollama"}
    except Exception as e:
        return {"status": "error", "service": "ollama", "detail": str(e)}


@router.get("")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_result, redis_result, ollama_result = await asyncio.gather(
        check_db(db),
        check_redis(),
        check_ollama(),
    )

    all_healthy = all(r["status"] == "ok" for r in [db_result, redis_result, ollama_result])

    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": [db_result, redis_result, ollama_result],
    }
