from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.social_posts import SocialPost
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/social", tags=["Social Media"])

class PostCreate(BaseModel):
    platform: str
    content: str
    scheduled_at: Optional[datetime] = None

@router.get("/posts")
async def get_posts(platform: str = None, status: str = None, db: AsyncSession = Depends(get_db)):
    query = select(SocialPost)
    if platform:
        query = query.where(SocialPost.platform == platform)
    if status:
        query = query.where(SocialPost.status == status)
    result = await db.execute(query.order_by(SocialPost.scheduled_at.desc()))
    return {"posts": result.scalars().all()}

@router.post("/posts")
async def create_post(data: PostCreate, db: AsyncSession = Depends(get_db)):
    post = SocialPost(platform=data.platform, content=data.content, scheduled_at=data.scheduled_at, status="draft" if not data.scheduled_at else "scheduled")
    db.add(post)
    await db.commit()
    return {"success": True, "post_id": post.id}
