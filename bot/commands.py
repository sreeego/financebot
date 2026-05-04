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