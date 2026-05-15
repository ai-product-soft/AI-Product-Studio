from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class LeadForm(Base):
    __tablename__ = "lead_forms"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    business_type = Column(String)
    budget_range = Column(String)
    timeline = Column(String)
    platform = Column(String)
    description = Column(Text)
    vision = Column(Text)
    requirements = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
