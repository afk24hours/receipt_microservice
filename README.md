**Микросервис для генерации чека в формате pdf с последующим созданием файла в локальной папке + отправки через Telegram bot**

1. git clone https://github.com/<your-username>/receipt_microservice.git
2. cd receipt_microservice
3. Создать .env файл
4. Внести токены и прочие ключи в файл .env
5. docker-compose up --build
6. uvicorn restapi:app --reload

7. Далее открываем http://127.0.0.1:8000/docs
8. Делаем POST запрос в /generate_receipt через swaggerUI 
9. Проверяете сгенерированный чек
10. Если вы умеете создавать ботов в телеге и после создания бота, получили токен бота, свой CHAT_ID и подписались на своего бота - он пришлет вам PDF файл

**внутри .env пишутся переменные**
# Telegram Bot
TELEGRAM_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_chat_id

# ClickHouse
CLICKHOUSE_HOST=clickhouse-server
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=user
CLICKHOUSE_PASSWORD=password
CLICKHOUSE_DB=receipts
