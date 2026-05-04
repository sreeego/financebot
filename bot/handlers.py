from telegram import Update
from telegram.ext import ContextTypes
from core.parser import parse_message
from core.database import add_transaction

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.effective_user.id)

    result = parse_message(text)
    if result:
        add_transaction(
            user_id=user_id,
            amount=result["amount"],
            type_=result["type"],
            category=result["category"],
            note=result["note"],
            date_=result["date"]
        )
        await update.message.set_reaction("👍")