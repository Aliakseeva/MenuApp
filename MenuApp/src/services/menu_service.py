from dataclasses import dataclass

from fastapi.encoders import jsonable_encoder

from MenuApp.src.services.cache_service import Cache
from MenuApp.src.services.db_service import create, read, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis import Redis
from fastapi import Depends, HTTPException

from MenuApp.src.db.schemas import MenuCreateUpdate, Menu


async def create_menu_service(menu: MenuCreateUpdate, db: AsyncSession):
    key = "/api/v1/menus"
    new_menu = await create.create_menu(db=db, menu=menu)
    if new_menu:
        await Cache.clear(key)
        return new_menu
    raise HTTPException(status_code=405, detail="Invalid input")


async def list_all_menus_service(db: AsyncSession):
    key = "/api/v1/menus"
    cached_l = await Cache.get(key)
    if cached_l:
        return cached_l
    menus_l = await read.get_menus(db=db)
    await Cache.set(key, jsonable_encoder(menus_l))
    return menus_l


async def get_menu_service(menu_id: int, db: AsyncSession):
    key = f"/api/v1/menus/{menu_id}"
    cached_menu = await Cache.get(key)
    if cached_menu:
        return cached_menu
    menu = await read.get_menu_by_id(db=db, menu_id=menu_id)
    if menu:
        await Cache.set(key, jsonable_encoder(menu))
        return menu
    raise HTTPException(status_code=404, detail="menu not found")


async def update_menu_service(
        menu_id: int,
        menu: MenuCreateUpdate,
        db: AsyncSession) -> dict[str, int]:
    key = f"/api/v1/menus/{menu_id}"
    upd_menu = await read.get_menu_by_id(db=db, menu_id=menu_id)
    if not upd_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    upd_menu.title = menu.title
    upd_menu.description = menu.description
    await Cache.set(key, jsonable_encoder(upd_menu))
    await update.update_menu(
        db=db, menu_id=menu_id, new_title=menu.title, new_descr=menu.description
    )
    return upd_menu


async def delete_menu_service(menu_id: int, db: AsyncSession) -> dict:
    key = "/api/v1/menus"
    del_menu = await delete.delete_menu(db=db, menu_id=menu_id)
    if del_menu:
        await Cache.clear(key)
        return {"status": True, "message": "The menu has been deleted"}
    raise HTTPException(status_code=404, detail="menu not found")
