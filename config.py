import os
import asyncio
from celery import Celery, chain
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import clickhouse_connect
import time
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", 8123))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
CLICKHOUSE_DB = os.getenv("CLICKHOUSE_DB")

# Папка куда сохраняются чеки
OUTPUT_DIR = "receipts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# RabbitMQ
celery = Celery(
    "tasks",
    broker="amqp://guest:guest@127.0.0.1:5672//",
    backend="rpc://"
)

# Clickhouse client
def get_clickhouse_client():
    retries = 10
    delay = 3
    for i in range(retries):
        try:
            client = clickhouse_connect.get_client(
                host=CLICKHOUSE_HOST,
                port=CLICKHOUSE_PORT,
                username=CLICKHOUSE_USER,
                password=CLICKHOUSE_PASSWORD,
                database=CLICKHOUSE_DB,
            )
            client.command("SELECT 1")
            return client
        except Exception as e:
            print(f"ClickHouse not ready, retry {i+1}/{retries}, waiting {delay}s...")
            time.sleep(delay)
    raise Exception("Cannot connect to ClickHouse")

