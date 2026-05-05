import io
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import openpyxl


def generate_pdf(transactions):
    now = date.today()
    monthly = [t for t in transactions if t.date.month == now.month and t.date.year == now.year]

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Finance Report — {now.strftime('%B %Y')}")

    income = sum(t.amount for t in monthly if t.type == "income")
    expenses = sum(t.amount for t in monthly if t.type == "expense")
    balance = income - expenses

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Income:   Rs.{income:,.0f}")
    c.drawString(50, height - 110, f"Expenses: Rs.{expenses:,.0f}")
    c.drawString(50, height - 130, f"Balance:  Rs.{balance:,.0f}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 170, "Transactions:")

    c.setFont("Helvetica", 10)
    y = height - 190
    for t in sorted(monthly, key=lambda x: x.date, reverse=True):
        sign = "+" if t.type == "income" else "-"
        line = f"{t.date}  {sign}Rs.{t.amount:,.0f}  {t.note}  [{t.category}]"
        c.drawString(50, y, line)
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    buf.seek(0)
    return buf


def generate_excel(transactions):
    now = date.today()
    monthly = [t for t in transactions if t.date.month == now.month and t.date.year == now.year]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = now.strftime("%B %Y")

    ws.append(["Date", "Type", "Amount", "Category", "Note"])
    for t in sorted(monthly, key=lambda x: x.date, reverse=True):
        ws.append([str(t.date), t.type, t.amount, t.category, t.note])

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf