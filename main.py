from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from bot.handlers import handle_message
from bot.commands import summary, history, undo, deletedata
from core.database import init_db
from dotenv import load_dotenv
import os

load_dotenv()
init_db()

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("history", history))
app.add_handler(CommandHandler("summary", summary))
app.add_handler(CommandHandler("undo", undo))
app.add_handler(CommandHandler("deletedata", deletedata))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()