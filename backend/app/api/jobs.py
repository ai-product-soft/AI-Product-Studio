from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.job import Job
from app.schemas.job import JobRead

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobRead)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/project/{project_id}", response_model=List[JobRead])
async def list_project_jobs(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Job).where(Job.project_id == project_id).order_by(Job.created_at.desc())
    )
    jobs = result.scalars().all()
    return jobs
