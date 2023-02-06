from typing import AsyncGenerator

import aioredis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

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

CACHE_REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
redis_client = aioredis.from_url(
    url=CACHE_REDIS_URL, db=REDIS_DB, decode_responses=True
)

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, future=True)  # optional: echo=True
Base = declarative_base()

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session
