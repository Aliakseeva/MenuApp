import asyncio
from collections.abc import AsyncGenerator

from httpx import AsyncClient
from pytest_asyncio import fixture

from MenuApp.src.database import async_session, engine, get_db
from MenuApp.src.main import app
from MenuApp.src.models import *

URL = "/api/v1/menus"
DATA = {"title": "Menu title", "description": "Menu description"}
UPDATED_DATA = {
    "title": "Upd menu title",
    "description": "Upd menu description",
}


@fixture
async def ac(db) -> AsyncClient:
    async def override_get_async_session():
        return db

    app.dependency_overrides[get_db] = override_get_async_session
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@fixture(autouse=True)
async def db() -> AsyncGenerator:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        yield db

    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture()
async def menu():
    async with async_session() as session:
        new_menu = Menu(**DATA)
        session.add(new_menu)
        await session.commit()

    return new_menu
