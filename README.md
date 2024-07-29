# Meme

---

## Структура

Микросервис разбит на слои:
- Domain
  - Model 
  - DTO
  - DAL
  - Service
- API

### Domain

    В него входит все сущности с их представление, бизнес-логикой, и способом получения.

### Model

    Слой данных (в данном случае Postgresql).

### DTO

    Слой промежуточного представления доменных сущностей.

### DAL

    Слой доступа к данным (в данном случае запросы к Postgresql).

### Service

    Слой логической валидации, обмена между DAL разных доменных сущностей.

### API

    Слой интерфейсов к внешним системам (роуты FastAPI)

---

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
---
## Концепция

### Стек
- FastAPI
- Postgresql
- Rabbitmq
- Minio

В проекте есть два микросервиса. Первый это API интерфейс для взаимодействия с фронтом. Второй это сервис для взаимодействия с Minio. Когда пользователь создает мем, он сохрнаняет картинку в Minio через второй сервис и записывает данные о меме в базу данных в первом сервисе. 

Чтобы не выводить огромную строку байт при выводе JSON информации о меме, вместо картинки отправляется ссылка на картинку. Ссылка ведет на другой ендпоинт .../images/..., где уже отображается конечная картинка.

---
## Тесты

Запуск тестов
> Для работы тестов нужно создать тестовую базу данных. Её название в [конфиге](https://github.com/WATUNeed/fastapi_meme/blob/master/meme/pytest.ini).

```
cd meme
```

```
poetry shell
```

```
python3 -m pytest -vv -c ./pytest.ini
```
