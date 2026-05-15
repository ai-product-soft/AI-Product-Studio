import asyncio
import json
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm import llm_chat, llm_embed
from app.services.scraper import scrape_search_results
from app.models.research_brief import ResearchBrief
from app.prompts.research import RESEARCH_PROMPT


async def generate_research_brief(
    db: AsyncSession,
    project_id: int,
    idea: str,
) -> ResearchBrief:
    queries = [
        f"{idea} market size",
        f"{idea} competitors",
        f"{idea} business model",
    ]

    all_results: List[Dict] = []
    for query in queries:
        results = await scrape_search_results(query, max_results=5)
        all_results.extend(results)
        await asyncio.sleep(1)

    search_text = "\n\n".join(
        f"Title: {r.get('title', '')}\nURL: {r.get('url', '')}\nSnippet: {r.get('snippet', '')}"
        for r in all_results
    )

    prompt = RESEARCH_PROMPT.format(idea=idea, search_results=search_text)
    messages = [{"role": "user", "content": prompt}]
    response = await llm_chat(messages, temperature=0.3, max_tokens=2048)

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        data = {
            "summary": "Could not parse structured research. Raw response attached.",
            "competitors": [],
            "opportunity_score": 50,
            "key_insights": [response[:500]],
        }

    embeddings = await llm_embed([data.get("summary", "")])
    embedding = embeddings[0] if embeddings else None

    brief = ResearchBrief(
        project_id=project_id,
        summary=data.get("summary", ""),
        competitors=data.get("competitors", []),
        opportunity_score=float(data.get("opportunity_score", 0)),
        key_insights=data.get("key_insights", []),
        raw_response=response,
        embedding=embedding,
    )

    db.add(brief)
    await db.commit()
    await db.refresh(brief)
    return brief
