from collections.abc import AsyncGenerator

from redis import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, REDIS_HOST, REDIS_PORT

CACHE_REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
pool = asyncio.ConnectionPool.from_url(CACHE_REDIS_URL)


async def get_redis():
    asyncio_redis = await asyncio.Redis(connection_pool=pool)
    yield asyncio_redis


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, future=True)  # optional: echo=True
Base = declarative_base()

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session
