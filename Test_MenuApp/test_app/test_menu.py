from httpx import AsyncClient
from pytest import mark

from ..conftest import DATA, UPDATED_DATA, URL, Menu


@mark.asyncio
async def test_create(ac: AsyncClient):
    response = await ac.post(URL, json=DATA)

    assert response.status_code == 201


@mark.asyncio
async def test_list_read(ac: AsyncClient, menu: Menu):
    response = await ac.get(URL)

    assert response.status_code == 200

    assert isinstance(response.json(), list)
    assert response.json()[0]["title"] == menu.title
    assert response.json()[0]["description"] == menu.description
    assert isinstance(response.json()[0]["id"], str)


@mark.asyncio
async def test_read(ac: AsyncClient, menu: Menu):
    response = await ac.get(f"{URL}/{menu.id}")

    assert response.status_code == 200

    assert response.json()["title"] == DATA["title"]
    assert response.json()["description"] == DATA["description"]
    assert isinstance(response.json()["id"], str)

    response404 = await ac.get(f"{URL}/0")
    assert response404.json() == dict(detail="menu not found")
    assert response404.status_code == 404


@mark.asyncio
async def test_patch(ac: AsyncClient, menu: Menu):
    response = await ac.patch(f"{URL}/{menu.id}", json=UPDATED_DATA)

    assert response.status_code == 200

    assert response.json()["id"] == str(menu.id)
    assert response.json()["title"] == UPDATED_DATA["title"]
    assert response.json()["description"] == UPDATED_DATA["description"]

    response404 = await ac.patch(f"{URL}/0", json=UPDATED_DATA)
    assert response404.status_code == 404
    assert response404.json() == dict(detail="menu not found")


@mark.asyncio
async def test_menu_delete(ac: AsyncClient, menu: Menu):
    response = await ac.delete(f"{URL}/{menu.id}")
    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "The menu has been deleted",
    }

    response404 = await ac.get(f"{URL}/{menu.id}")
    assert response404.status_code == 404
    assert response404.json() == dict(detail="menu not found")
