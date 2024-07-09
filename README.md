# Meme
Тестовое задание

## Деплой

1. Клонировать репозиротий
   ```
   git clone git@github.com:WATUNeed/fastapi_meme.git
   ```
   
2. Создать переменные окружения
   ```
   # .env в корне проекта

   # Postgres
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=meme_database
   POSTGRES_DRIVER='postgresql+asyncpg'

   # Rabbitmq
   RABBITMQ_HOST=rabbitmq
   RABBITMQ_PORT=5672
   RABBITMQ_DEFAULT_USER=guest
   RABBITMQ_DEFAULT_PASS=guest
   RABBITMQ_VHOST=

   # Minio
   MINIO_HOST=minio
   MINIO_PORT=9000
   MINIO_USER=ROOTNAME
   MINIO_PASSWORD=CHANGEME123
   MINIO_ACCESS_KEY=...  # from minio web interface http://localhost:9000/
   MINIO_SECRET_KEY=...  # from minio web interface http://localhost:9000/

   # Meme (FastAPI backend)
   MEME_PORT=8000
   MEME_HOST=meme
   MEME_DEBUG=True
   MEME_ORIGIN=http://localhost:$MEME_PORT

   # Compose paths
   BACKEND_YML=backend.yml
   INFRASTRUCTURE_YML=infrastructure.yml
   ```
   
3. Запускаем проект из корня
   ```
   docker compose up -d --build
   ```
   
4. [Документация](http://localhost:8000/docs)
