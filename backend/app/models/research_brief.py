from sqlalchemy import Column, Integer, Text, Float, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.db.base import Base


class ResearchBrief(Base):
    __tablename__ = "research_briefs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    summary = Column(Text, nullable=True)
    competitors = Column(JSONB, nullable=True)
    opportunity_score = Column(Float, nullable=True)
    key_insights = Column(JSONB, nullable=True)
    raw_response = Column(Text, nullable=True)
    embedding = Column(Vector(768), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="research_briefs")
