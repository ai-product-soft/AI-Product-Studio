from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProjectPlan(Base):
    __tablename__ = "project_plans"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    phases = Column(JSONB, nullable=True)
    tech_stack = Column(JSONB, nullable=True)
    monetization_strategy = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="project_plans")
