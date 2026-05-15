import os
import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm import llm_chat
from app.prompts.landing import LANDING_PROMPT


async def generate_landing_page(
    db: AsyncSession,
    project_id: int,
    idea: str,
    plan: dict,
    output_dir: str,
) -> str:
    prompt = LANDING_PROMPT.format(
        idea=idea,
        product_name=plan.get("product_name", idea),
        description=plan.get("description", idea),
        features=json.dumps(plan.get("features", [])),
    )
    messages = [{"role": "user", "content": prompt}]
    html = await llm_chat(messages, temperature=0.6, max_tokens=4096)

    if "```html" in html:
        html = html.split("```html")[1].split("```")[0].strip()

    landing_dir = os.path.join(output_dir, "landing")
    os.makedirs(landing_dir, exist_ok=True)
    landing_path = os.path.join(landing_dir, "index.html")

    with open(landing_path, "w", encoding="utf-8") as f:
        f.write(html)

    return landing_path
