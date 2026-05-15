import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm import llm_chat
from app.models.project_plan import ProjectPlan
from app.prompts.plan import PLAN_PROMPT


async def generate_project_plan(
    db: AsyncSession,
    project_id: int,
    idea: str,
    research_summary: str,
) -> ProjectPlan:
    prompt = PLAN_PROMPT.format(idea=idea, research_summary=research_summary)
    messages = [{"role": "user", "content": prompt}]
    response = await llm_chat(messages, temperature=0.4, max_tokens=4096)

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        data = {
            "phases": [],
            "tech_stack": {},
            "monetization_strategy": response[:1000],
        }

    plan = ProjectPlan(
        project_id=project_id,
        phases=data.get("phases", []),
        tech_stack=data.get("tech_stack", {}),
        monetization_strategy=data.get("monetization_strategy", ""),
    )

    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan
