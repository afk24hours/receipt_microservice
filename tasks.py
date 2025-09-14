import os
import asyncio
from celery import Celery
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from telegram import Bot
from telegram_tasks import *
from config import *

@celery.task
def generate_pdf_task(data: dict):
    shop_name = data.get("shop_name", "Shop")
    items = data.get("items", [])
    task_id = generate_pdf_task.request.id
    created_at = datetime.now()
    file_path = os.path.join(OUTPUT_DIR, f"receipt_{task_id}.pdf")

    # Генерация PDF
    pdf = canvas.Canvas(file_path, pagesize=A4)
    pdf.setFont("Helvetica", 14)
    pdf.drawString(100, 800, f"Shop: {shop_name}")
    y = 770
    total = 0
    for item in items:
        name = item.get("name", "???")
        price = item.get("price", 0)
        qty = item.get("qty", 1)
        subtotal = price * qty
        total += subtotal
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, y, f"{name} x {qty} = {subtotal:.2f} KZT")
        y -= 20
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, y - 20, f"Total: {total:.2f} KZT")
    pdf.showPage()
    pdf.save()

    check_details = {
        "task_id": task_id,
        "shop_name": shop_name,
        "total": total,
        "created_at": created_at,
        "file_path": file_path,
    }

    # Сохранение данных чека в ClickHouse
    save_to_clickhouse_task.delay(check_details)
    # Запуск таска для Telegram
    send_pdf_task.delay(file_path, shop_name, total)

    return {"file_path": file_path, "total": total}

@celery.task
def send_pdf_task(file_path: str, shop_name: str, total: float):
    bot = Bot(token=TELEGRAM_TOKEN)
    caption = f"Новый чек: {shop_name}\nИтого: {total:.2f} KZT"

    async def _send():
        with open(file_path, "rb") as f:
            await bot.send_document(chat_id=TELEGRAM_CHAT_ID, document=f, caption=caption)

    asyncio.run(_send())

@celery.task
def save_to_clickhouse_task(data: dict):
    client = get_clickhouse_client()
    row = [[data["task_id"], data["shop_name"], data["total"], data["created_at"]]]
    client.insert(
        table="checks",
        data=row,
        column_names=["id", "shop_name", "total", "created_at"]
    )
    return data