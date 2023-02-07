from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from MenuApp.src.db.config import settings


engine = create_async_engine(settings.DB_URL, future=True)  # optional: echo=True
Base = declarative_base()

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session
