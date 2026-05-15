import json
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm import llm_chat
from app.models.ad_campaign import AdCampaign
from app.prompts.ads import GOOGLE_ADS_PROMPT, FACEBOOK_ADS_PROMPT


async def generate_ad_creatives(
    db: AsyncSession,
    project_id: int,
    idea: str,
    plan: dict,
    target_audience: str = "general",
) -> Dict[str, AdCampaign]:
    campaigns = {}

    google_prompt = GOOGLE_ADS_PROMPT.format(
        idea=idea,
        target_audience=target_audience,
        features=json.dumps(plan.get("features", [])),
    )
    messages = [{"role": "user", "content": google_prompt}]
    google_response = await llm_chat(messages, temperature=0.7, max_tokens=2048)

    try:
        google_data = json.loads(google_response)
    except json.JSONDecodeError:
        google_data = {"headlines": [idea], "descriptions": ["Best solution for your needs."]}

    google_campaign = AdCampaign(
        project_id=project_id,
        platform="google",
        ad_copy=google_data,
    )
    db.add(google_campaign)
    campaigns["google"] = google_campaign

    fb_prompt = FACEBOOK_ADS_PROMPT.format(
        idea=idea,
        target_audience=target_audience,
        features=json.dumps(plan.get("features", [])),
    )
    messages = [{"role": "user", "content": fb_prompt}]
    fb_response = await llm_chat(messages, temperature=0.7, max_tokens=2048)

    try:
        fb_data = json.loads(fb_response)
    except json.JSONDecodeError:
        fb_data = {"primary_text": idea, "headlines": [idea], "descriptions": ["Try it now."]}

    fb_campaign = AdCampaign(
        project_id=project_id,
        platform="facebook",
        ad_copy=fb_data,
    )
    db.add(fb_campaign)
    campaigns["facebook"] = fb_campaign

    await db.commit()
    for c in campaigns.values():
        await db.refresh(c)

    return campaigns
