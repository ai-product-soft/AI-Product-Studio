from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class MCPServer(Base):
    __tablename__ = "mcp_servers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    display_name = Column(String)
    description = Column(Text)
    server_type = Column(String)
    config = Column(JSON, default=dict)
    is_free = Column(Boolean, default=True)
    cost_per_month = Column(Integer, default=0)
    status = Column(String, default="disconnected")
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
