1. git clone https://github.com/<your-username>/receipt_microservice.git
2. cd receipt_microservice
3. Создать .env файл
4. Внести токены и прочие ключи в файл .env
5. docker-compose up --build
6. uvicorn restapi:app --reload

# внутри .env пишутся переменные
# Telegram Bot
TELEGRAM_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_chat_id

# ClickHouse
CLICKHOUSE_HOST=clickhouse-server
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=user
CLICKHOUSE_PASSWORD=password
CLICKHOUSE_DB=receipts
