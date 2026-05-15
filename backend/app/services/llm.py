import httpx
from typing import List, Dict, Any

from app.config import settings


async def llm_chat(
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 2048,
    format: str = None,
) -> str:
    payload: Dict[str, Any] = {
        "model": settings.OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    if format:
        payload["format"] = format

    async with httpx.AsyncClient(timeout=300.0) as client:
        resp = await client.post(
            f"{settings.OLLAMA_URL}/api/chat",
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["message"]["content"]


async def llm_embed(texts: List[str]) -> List[List[float]]:
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{settings.OLLAMA_URL}/api/embed",
            json={"model": settings.EMBED_MODEL, "input": texts},
        )
        resp.raise_for_status()
        data = resp.json()
        return data["embeddings"]
