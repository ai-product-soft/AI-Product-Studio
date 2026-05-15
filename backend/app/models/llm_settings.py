from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class LLMSettings(Base):
    __tablename__ = "llm_settings"
    id = Column(Integer, primary_key=True, index=True)
    primary_provider = Column(String, default="google")
    primary_model = Column(String, default="gemini-2.5-flash")
    primary_api_key = Column(String, nullable=True)
    fallback_1_provider = Column(String, default="groq")
    fallback_1_model = Column(String, default="llama-3.3-70b")
    fallback_1_api_key = Column(String, nullable=True)
    fallback_2_provider = Column(String, default="cerebras")
    fallback_2_model = Column(String, default="llama-3.3-70b")
    fallback_2_api_key = Column(String, nullable=True)
    fallback_3_provider = Column(String, default="openrouter")
    fallback_3_model = Column(String, default="auto")
    fallback_3_api_key = Column(String, nullable=True)
    local_model = Column(String, default="gemma3:4b")
    ollama_url = Column(String, default="http://ollama:11434")
    auto_switch = Column(Boolean, default=True)
    timeout_seconds = Column(Integer, default=30)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
