from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    amount = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    method = Column(String)
    status = Column(String, default="pending")
    stripe_payment_intent = Column(String, nullable=True)
    upi_transaction_id = Column(String, nullable=True)
    bank_reference = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
