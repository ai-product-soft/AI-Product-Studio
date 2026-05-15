import enum

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProjectStatus(str, enum.Enum):
    IDEA = "idea"
    RESEARCHING = "researching"
    RESEARCH_COMPLETE = "research_complete"
    PLANNING = "planning"
    PLAN_COMPLETE = "plan_complete"
    GENERATING = "generating"
    GENERATION_REVIEW = "generation_review"
    PROMOTING = "promoting"
    SALES_READY = "sales_ready"
    COMPLETED = "completed"
    FAILED = "failed"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    client_idea = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default=ProjectStatus.IDEA)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    jobs = relationship("Job", back_populates="project", cascade="all, delete-orphan")
    research_briefs = relationship("ResearchBrief", back_populates="project", cascade="all, delete-orphan")
    project_plans = relationship("ProjectPlan", back_populates="project", cascade="all, delete-orphan")
    ad_campaigns = relationship("AdCampaign", back_populates="project", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="project", cascade="all, delete-orphan")
