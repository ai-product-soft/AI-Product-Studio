from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class Proposal(Base):
    __tablename__ = "proposals"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    lead_id = Column(Integer, ForeignKey("leads.id"))
    title = Column(String)
    client_name = Column(String)
    vision_summary = Column(Text)
    improvements = Column(JSON, default=list)
    workflow = Column(Text)
    investment = Column(Float, default=0.0)
    timeline_weeks = Column(Integer, default=4)
    status = Column(String, default="draft")
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
