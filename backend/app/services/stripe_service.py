import os
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
import stripe as stripe_lib

from app.config import settings
from app.models.invoice import Invoice

stripe_lib.api_key = settings.STRIPE_API_KEY


async def create_payment_link(
    db: AsyncSession,
    project_id: int,
    amount: int,
    currency: str = "usd",
    project_name: str = "AI Product Studio Deliverable",
) -> Invoice:
    product = stripe_lib.Product.create(name=f"{project_name} - Project {project_id}")
    price = stripe_lib.Price.create(
        unit_amount=amount,
        currency=currency,
        product=product.id,
    )

    payment_link = stripe_lib.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}],
    )

    invoice = Invoice(
        project_id=project_id,
        stripe_payment_link=payment_link.url,
        amount=amount,
        currency=currency,
        status="pending",
    )

    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return invoice


async def generate_invoice_pdf(
    invoice: Invoice,
    project_name: str,
    output_path: str,
) -> str:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("INVOICE", styles["Heading1"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"<b>Project:</b> {project_name}", styles["Normal"]))
    story.append(Paragraph(f"<b>Invoice ID:</b> {invoice.id}", styles["Normal"]))
    story.append(Paragraph(f"<b>Amount:</b> ${invoice.amount / 100:.2f} {invoice.currency.upper()}", styles["Normal"]))
    story.append(Paragraph(f"<b>Status:</b> {invoice.status.upper()}", styles["Normal"]))
    if invoice.stripe_payment_link:
        story.append(Paragraph(f"<b>Payment Link:</b> {invoice.stripe_payment_link}", styles["Normal"]))
    story.append(Spacer(1, 24))

    data = [["Description", "Amount"]]
    data.append([f"AI Product Studio - {project_name}", f"${invoice.amount / 100:.2f}"])
    data.append(["Total", f"${invoice.amount / 100:.2f}"])

    table = Table(data, colWidths=[400, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    story.append(table)
    doc.build(story)

    return output_path
