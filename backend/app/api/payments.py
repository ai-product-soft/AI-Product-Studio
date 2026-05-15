from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.session import get_db
from app.models.payments import Payment
from app.models.invoices import Invoice
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/payments", tags=["Payments"])

class PaymentCreate(BaseModel):
    project_id: int
    amount: float
    method: str

@router.get("/")
async def list_payments(method: str = None, status: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Payment)
    if method:
        query = query.where(Payment.method == method)
    if status:
        query = query.where(Payment.status == status)
    result = await db.execute(query.order_by(Payment.created_at.desc()))
    return {"payments": result.scalars().all()}

@router.get("/revenue")
async def get_revenue(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(func.sum(Payment.amount)).where(Payment.status == "completed"))
    total = result.scalar() or 0
    from sqlalchemy import extract
    monthly = await db.execute(select(extract('month', Payment.created_at).label('month'), func.sum(Payment.amount).label('total')).where(Payment.status == "completed").group_by(extract('month', Payment.created_at)))
    return {"total_revenue": total, "monthly": [{"month": m.month, "total": m.total} for m in monthly.all()]}

@router.post("/")
async def create_payment(data: PaymentCreate, db: AsyncSession = Depends(get_db)):
    payment = Payment(**data.dict(), status="pending")
    db.add(payment)
    await db.commit()
    return {"success": True, "payment_id": payment.id}
