import redis
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


from .config import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PORT,
)

LOCAL_REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True,
)

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# engine = create_engine(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
Base = declarative_base()

# local_session = sessionmaker(bind=engine)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


# def get_db() -> Session:
#     """Create session generator to establish all conversations with the database"""
#     db = local_session()
#     try:
#         yield db
#     finally:
#         db.close()
