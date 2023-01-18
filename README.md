# MenuApp
Restaraunt menu REST API
<!--  DELETE THE LINES ABOVE THIS AND WRITE YOUR PROJECT README BELOW -->

# Based on:
```
🐍 Python3
⚡ FastAPI Web framework
🐘 PostgreSQL
📜 SQLAlchemy ORM
📝 Alembic database migration tool
🦄 Uvicorn ASGI web server
```

# 1. Clone repository

```bash
git clone https://github.com/Aliakseeva/MenuApp
```

# 2. Set up .evn file, for example:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
```

# 3. Create virtual environment and activate it

Make sure you are located in /MenuApp repository!

```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
``` 

# 4. Install requirements

```bash
pip install -r requirements.txt
```

# 5. Apply migrations

```bash
alembic upgrade head
```

# 6. Run the project

```bash
uvicorn src.main:app --reload
```

Note! The database is cleared automatically with every app run.

# 7. You are awesome! Enjoy! 😼
