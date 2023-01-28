from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import redis

from .config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, REDIS_HOST, REDIS_PORT, REDIS_DB


LOCAL_REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL)
Base = declarative_base()

local_session = sessionmaker(bind=engine)


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

