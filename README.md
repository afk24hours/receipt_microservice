1. git clone https://github.com/<your-username>/receipt_microservice.git
2. cd receipt_microservice
3. Создать .env файл
4. Внести токены и прочие ключи в файл .env
5. docker-compose up --build
6. uvicorn restapi:app --reload
