import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# Отправка чека в Telegram
async def send_pdf(file_path: str, caption: str = ""):
    with open(file_path, "rb") as f:
        await bot.send_document(chat_id=TELEGRAM_CHAT_ID, document=f, caption=caption)