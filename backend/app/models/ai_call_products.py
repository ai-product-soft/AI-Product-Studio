from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class AICallProduct(Base):
    __tablename__ = "ai_call_products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    config = Column(JSON, default=dict)
    voice_settings = Column(JSON, default=dict)
    script_template = Column(Text)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
