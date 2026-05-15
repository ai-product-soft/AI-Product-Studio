from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.project import Project, ProjectStatus
from app.models.job import Job, JobType, JobStatus
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.workers.research_worker import run_research_task
from app.workers.plan_worker import run_plan_task
from app.workers.generation_worker import run_generation_task
from app.workers.promotion_worker import run_promotion_task
from app.workers.sales_worker import run_sales_task

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project = Project(name=data.name, client_idea=data.client_idea, status=ProjectStatus.IDEA)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.get("", response_model=List[ProjectRead])
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    projects = result.scalars().all()
    return projects


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id)
        .options(
            selectinload(Project.jobs),
            selectinload(Project.research_briefs),
            selectinload(Project.project_plans),
            selectinload(Project.ad_campaigns),
            selectinload(Project.invoices),
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(project_id: int, data: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if data.name is not None:
        project.name = data.name
    if data.client_idea is not None:
        project.client_idea = data.client_idea
    if data.status is not None:
        project.status = data.status

    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(project)
    await db.commit()
    return None


async def _create_job(db: AsyncSession, project_id: int, job_type: str) -> Job:
    job = Job(project_id=project_id, job_type=job_type, status=JobStatus.PENDING)
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def _update_project_status(db: AsyncSession, project_id: int, status: str):
    await db.execute(
        update(Project)
        .where(Project.id == project_id)
        .values(status=status)
    )
    await db.commit()


@router.post("/{project_id}/research", response_model=dict)
async def start_research(project_id: int, db: AsyncSession = Depends(get_db)):
    job = await _create_job(db, project_id, JobType.RESEARCH)
    await _update_project_status(db, project_id, ProjectStatus.RESEARCHING)

    task = run_research_task.delay(project_id, job.id)
    job.celery_task_id = task.id
    job.status = JobStatus.RUNNING
    await db.commit()

    return {"message": "Research started", "job_id": job.id, "task_id": task.id}


@router.post("/{project_id}/plan", response_model=dict)
async def start_plan(project_id: int, db: AsyncSession = Depends(get_db)):
    job = await _create_job(db, project_id, JobType.PLAN)
    await _update_project_status(db, project_id, ProjectStatus.PLANNING)

    task = run_plan_task.delay(project_id, job.id)
    job.celery_task_id = task.id
    job.status = JobStatus.RUNNING
    await db.commit()

    return {"message": "Planning started", "job_id": job.id, "task_id": task.id}


@router.post("/{project_id}/generate", response_model=dict)
async def start_generation(project_id: int, db: AsyncSession = Depends(get_db)):
    job = await _create_job(db, project_id, JobType.GENERATE)
    await _update_project_status(db, project_id, ProjectStatus.GENERATING)

    task = run_generation_task.delay(project_id, job.id)
    job.celery_task_id = task.id
    job.status = JobStatus.RUNNING
    await db.commit()

    return {"message": "Generation started", "job_id": job.id, "task_id": task.id}


@router.post("/{project_id}/promote", response_model=dict)
async def start_promotion(project_id: int, db: AsyncSession = Depends(get_db)):
    job = await _create_job(db, project_id, JobType.PROMOTE)
    await _update_project_status(db, project_id, ProjectStatus.PROMOTING)

    task = run_promotion_task.delay(project_id, job.id)
    job.celery_task_id = task.id
    job.status = JobStatus.RUNNING
    await db.commit()

    return {"message": "Promotion started", "job_id": job.id, "task_id": task.id}


@router.post("/{project_id}/sales", response_model=dict)
async def start_sales(project_id: int, db: AsyncSession = Depends(get_db)):
    job = await _create_job(db, project_id, JobType.SALES)
    await _update_project_status(db, project_id, ProjectStatus.SALES_READY)

    task = run_sales_task.delay(project_id, job.id)
    job.celery_task_id = task.id
    job.status = JobStatus.RUNNING
    await db.commit()

    return {"message": "Sales started", "job_id": job.id, "task_id": task.id}
