from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    stripe_payment_intent_id = Column(String(255), nullable=True)
    stripe_payment_link = Column(String(500), nullable=True)
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False, default="usd")
    status = Column(String(50), nullable=False, default="pending")
    pdf_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="invoices")
