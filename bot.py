# bot.py
import os
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

if not bot_token or not chat_id:
    raise ValueError("Please set TELEGRAM_BOT_TOKEN and CHAT_ID in your environment variables.")

bot = Bot(token=bot_token)
application = Application.builder().token(bot_token).build()

# Global to store last signal message
last_signal = "No signals yet."

async def send_signal(message: str):
    global last_signal
    last_signal = message
    await bot.send_message(chat_id=chat_id, text=message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! The EUR/USD Liquidity Grab Bot is active and monitoring the market."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is active and monitoring the market every minute.")

async def last_signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📊 Last Signal:\n{last_signal}")

def update_last_signal(message: str):
    global last_signal
    last_signal = message

# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("lastsignal", last_signal_command))
