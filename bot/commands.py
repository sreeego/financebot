from telegram import Update
from telegram.ext import ContextTypes
from core.database import get_transactions, get_session, Transaction, set_budget, get_budgets
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

async def undo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    session = get_session(user_id)

    last = session.query(Transaction).order_by(Transaction.id.desc()).first()

    if not last:
        await update.message.reply_text("Nothing to undo.")
        session.close()
        return

    session.delete(last)
    session.commit()
    session.close()

    await update.message.reply_text(f"↩️ Removed: {'+'if last.type == 'income' else '-'}₹{last.amount:,.0f} {last.note}")

async def deletedata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    import os

    db_path = f"data/{user_id}.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        await update.message.reply_text("🗑️ All your data has been deleted.")
    else:
        await update.message.reply_text("No data found.")

async def budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if context.args and len(context.args) == 2:
        category, limit = context.args[0].lower(), float(context.args[1])
        set_budget(user_id, category, limit)
        await update.message.reply_text(f"✅ Budget set: ₹{limit:,.0f} for {category}")
        return

    budgets = get_budgets(user_id)
    if not budgets:
        await update.message.reply_text("No budgets set.\nUse: /budget food 3000")
        return

    now = date.today()
    transactions = get_transactions(user_id)
    monthly = [t for t in transactions if t.date.month == now.month and t.date.year == now.year]

    lines = []
    for b in budgets:
        spent = sum(t.amount for t in monthly if t.category == b.category and t.type == "expense")
        percent = (spent / b.limit) * 100 if b.limit else 0
        status = "🔴" if percent >= 100 else "🟡" if percent >= 80 else "🟢"
        lines.append(f"{status} {b.category}: ₹{spent:,.0f} / ₹{b.limit:,.0f} ({percent:.0f}%)")

    await update.message.reply_text("💰 Budget Status\n\n" + "\n".join(lines))

async def graph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    transactions = get_transactions(user_id)

    from reports.graph import generate_graph
    buf = generate_graph(transactions)

    if not buf:
        await update.message.reply_text("No expenses found for this month.")
        return

    await update.message.reply_photo(photo=buf, caption="📊 This month's spending breakdown")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    transactions = get_transactions(user_id)

    from reports.export import generate_pdf, generate_excel

    if context.args and context.args[0].lower() == "excel":
        buf = generate_excel(transactions)
        await update.message.reply_document(document=buf, filename="report.xlsx", caption="📊 Your Excel report")
    else:
        buf = generate_pdf(transactions)
        await update.message.reply_document(document=buf, filename="report.pdf", caption="📊 Your PDF report")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if not context.args:
        await update.message.reply_text("Usage: /ask how much did I spend on food?")
        return

    question = " ".join(context.args)
    transactions = get_transactions(user_id)

    from ai.ask import ask_ai
    await update.message.reply_text("🤔 Thinking...")
    answer = ask_ai(question, transactions)
    await update.message.reply_text(answer)

