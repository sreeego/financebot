from telegram import Update
from telegram.ext import ContextTypes
from core.database import get_transactions
from datetime import date

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    transactions = get_transactions(user_id)

    now = date.today()
    monthly = [t for t in transactions if t.date.month == now.month and t.date.year == now.year]

    income = sum(t.amount for t in monthly if t.type == "income")
    expenses = sum(t.amount for t in monthly if t.type == "expense")
    balance = income - expenses

    await update.message.reply_text(
        f"📊 This Month's Summary\n\n"
        f"Income:    ₹{income:,.0f}\n"
        f"Expenses:  ₹{expenses:,.0f}\n"
        f"Balance:   ₹{balance:,.0f}"
    )

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    transactions = get_transactions(user_id)

    if not transactions:
        await update.message.reply_text("No transactions found.")
        return

    last10 = sorted(transactions, key=lambda t: t.date, reverse=True)[:10]

    lines = []
    for t in last10:
        sign = "+" if t.type == "income" else "-"
        lines.append(f"{sign}₹{t.amount:,.0f} {t.note} ({t.date})")

    await update.message.reply_text("🧾 Last 10 Transactions\n\n" + "\n".join(lines))