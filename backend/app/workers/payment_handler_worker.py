from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.models.payments import Payment
from app.models.invoices import Invoice
from app.services.notification import notification_service
import asyncio
import uuid

@shared_task(bind=True, max_retries=2)
def run_payment_handler_task(self, project_id, amount, method, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                payment = Payment(project_id=project_id, amount=amount, method=method, status="pending")
                db.add(payment)
                await db.commit()
                invoice = Invoice(project_id=project_id, payment_id=payment.id, invoice_number=f"APS-{uuid.uuid4().hex[:8].upper()}", amount=amount, status="draft")
                db.add(invoice)
                await db.commit()
                if method == "stripe":
                    payment.status = "completed"
                    payment.stripe_payment_intent = f"pi_{uuid.uuid4().hex}"
                elif method == "upi":
                    payment.status = "completed"
                    payment.upi_transaction_id = f"UPI{uuid.uuid4().hex[:12].upper()}"
                elif method == "bank_transfer":
                    payment.status = "pending"
                    payment.bank_reference = f"BANK{uuid.uuid4().hex[:10].upper()}"
                invoice.status = "sent" if payment.status == "completed" else "draft"
                job.status = JobStatus.COMPLETED
                job.result = {"payment_id": payment.id, "invoice_id": invoice.id, "status": payment.status}
                await db.commit()
                if payment.status == "completed":
                    await notification_service.create_payment_notification(amount, project.name)
                return {"status": "completed", "payment_status": payment.status}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
