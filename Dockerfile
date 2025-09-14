FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Переменные окружения
ENV CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
ENV CELERY_BACKEND=rpc://
ENV CLICKHOUSE_HOST=clickhouse-server
ENV CLICKHOUSE_PORT=8123
ENV CLICKHOUSE_USER=user
ENV CLICKHOUSE_PASSWORD=password
ENV CLICKHOUSE_DB=receipts

CMD ["sh", "-c", "sleep 10 && celery -A tasks worker --loglevel=info"]

# Запуск Celery воркера
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]