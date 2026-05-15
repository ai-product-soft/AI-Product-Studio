from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.showcases import Showcase
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/showcases", tags=["Showcases"])

@router.get("/")
async def list_showcases(featured: bool = None, db: AsyncSession = Depends(get_db)):
    query = select(Showcase)
    if featured:
        query = query.where(Showcase.is_featured == True)
    result = await db.execute(query.order_by(Showcase.created_at.desc()))
    return {"showcases": result.scalars().all()}

@router.get("/{showcase_id}")
async def get_showcase(showcase_id: int, db: AsyncSession = Depends(get_db)):
    showcase = await db.get(Showcase, showcase_id)
    if not showcase:
        return {"error": "Showcase not found"}
    return {"showcase": showcase}
