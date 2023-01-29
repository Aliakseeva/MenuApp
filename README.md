# MenuApp
Restaurant menu REST API


# Based on:
```
🐍 Python3
⚡ FastAPI Web framework
🐘 PostgreSQL database
⏳ Redis-cache
📜 SQLAlchemy ORM
📝 Alembic database migration tool
🦄 Uvicorn ASGI web server
🐳 Docker containers
✅ Pytest
```

# DOCKER RUN


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

# MANUAL RUN


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

##### 6. Run redis-server and start the project:

```bash
redis-server
uvicorn src.main:app --reload
```

Note! The database is cleared automatically with every app run.

##### 7. You are awesome! Enjoy! 😼
