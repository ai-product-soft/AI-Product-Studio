from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.services import Service
from app.models.service_packages import ServicePackage

router = APIRouter(prefix="/services", tags=["Services"])

@router.get("/")
async def list_services(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).where(Service.is_active == True))
    return {"services": result.scalars().all()}

@router.get("/packages")
async def list_packages(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ServicePackage))
    return {"packages": result.scalars().all()}
