from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class ServicePackage(Base):
    __tablename__ = "service_packages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    display_name = Column(String)
    description = Column(Text)
    services = Column(JSON, default=list)
    price = Column(Float, default=0.0)
    timeline_weeks = Column(Integer, default=4)
    is_popular = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
