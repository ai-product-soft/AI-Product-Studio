import json
import os
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm import llm_chat


async def generate_content(
    db: AsyncSession,
    project_id: int,
    idea: str,
    plan: dict,
    output_dir: str,
) -> Dict[str, str]:
    content_dir = os.path.join(output_dir, "promo")
    os.makedirs(content_dir, exist_ok=True)

    blog_prompt = f"""Write a comprehensive, SEO-optimized blog post about "{idea}".
Include: introduction, key benefits, use cases, and conclusion.
Target keywords: {idea}, AI automation, productivity.
Output in markdown format. Do not include a title header."""
    messages = [{"role": "user", "content": blog_prompt}]
    blog_post = await llm_chat(messages, temperature=0.7, max_tokens=4096)

    blog_path = os.path.join(content_dir, "blog_post.md")
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(blog_post)

    social_prompt = f"""Generate 5 social media posts for Twitter/X and LinkedIn about "{idea}".
For each post, provide:
- platform (twitter or linkedin)
- text (under 280 chars for twitter, under 3000 for linkedin)
- hashtags (3-5 relevant tags)
Output as JSON array."""
    messages = [{"role": "user", "content": social_prompt}]
    social_response = await llm_chat(messages, temperature=0.8, max_tokens=2048)

    try:
        social_posts = json.loads(social_response)
    except json.JSONDecodeError:
        social_posts = [
            {"platform": "twitter", "text": f"Check out {idea}! #AI #Tech", "hashtags": ["#AI", "#Tech"]}
        ]

    social_path = os.path.join(content_dir, "social_posts.json")
    with open(social_path, "w", encoding="utf-8") as f:
        json.dump(social_posts, f, indent=2)

    return {
        "blog_post": blog_path,
        "social_posts": social_path,
    }
