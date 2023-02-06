# MenuApp
Restaurant menu REST API with CRUD-operations, cache and pancakes!

See OpenAPI Specification: http://0.0.0.0:8000/

## Based on:
```
🐍 Python3
⚡ FastAPI Web framework
🐘 PostgreSQL database
⏳ Redis-cache
📜 SQLAlchemy ORM
📝 Alembic database migration tool
🦄 Uvicorn ASGI web server
🐳 Docker containers
🥦 Celery-tasks
🐰 RabbitMQ broker
✅ Pytest
```

## DOCKER RUN:


##### 1. Clone repository:

```bash
git clone https://github.com/Aliakseeva/MenuApp
```

##### 2. Run docker-compose:

Make sure you are located in project repository!

```bash
docker-compose up
```

##### 3. Done! Wanna test it? Run:

```bash
docker-compose -f docker-compose-tests.yml up
```

## MANUAL RUN:


##### 1. Clone repository:

```bash
git clone https://github.com/Aliakseeva/MenuApp
```

##### 2. Set up .evn file, for example:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

RABBITMQ_HOST=rabbit
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=rabbit
RABBITMQ_DEFAULT_PASS=rabbit
RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS='-rabbit disk_free_limit 2147483648'
```

##### 3. Create virtual environment and activate it:

Make sure you are located in project repository!

```bash
python -m venv venv
source MenuApp/venv/Scripts/activate
```

##### 4. Install requirements:

```bash
pip install -r MenuApp/requirements.txt
```

##### 5. Apply migrations:

```bash
cd MenuApp/
alembic upgrade head
```

##### 6. Run redis, rabbit servers, and start the project:

```bash
redis-server
docker run -d -p 5672:5672 rabbit
uvicorn src.main:app --reload
```

##### 7. You are awesome! Enjoy! 😼
