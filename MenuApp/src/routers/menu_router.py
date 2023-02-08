from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.cache import Cache
from MenuApp.src.database import get_db
from MenuApp.src.routers.custom_APIRouter import APIRouter
from MenuApp.src.schemas import menu_schemas as m
from MenuApp.src.services.crud import create, delete, read, update

router = APIRouter(tags=["Menu"], prefix="/api/v1/menus")


@router.post(
    "/",
    response_model=m.Menu,
    summary="Create a new menu",
    status_code=HTTPStatus.CREATED,
)
async def create_menu(
    menu: m.MenuCreateUpdate, db: AsyncSession = Depends(get_db)
) -> dict[str, int]:
    """Create a Menu-record in database.
    Specify the title and the description to set."""
    key = "/api/v1/menus"
    new_menu = await create.create_menu(db=db, menu=menu)
    if new_menu:
        await Cache.clear_cache(key)
        return new_menu
    raise HTTPException(status_code=405, detail="Invalid input")


@router.get(
    "/",
    response_model=list[m.Menu],
    summary="Get a menus list",
    status_code=HTTPStatus.OK,
)
async def get_all_menus(db: AsyncSession = Depends(get_db)):
    """Get all Menu-records and their details from database in list."""
    key = "/api/v1/menus"
    cached_l = await Cache.get_from_cache(router.prefix)
    if cached_l:
        return cached_l
    menus_l = await read.get_menus(db=db)
    await Cache.set_to_cache(key, jsonable_encoder(menus_l))
    return menus_l


@router.get(
    "/{menu_id}",
    response_model=m.Menu,
    summary="Get menu details",
    status_code=HTTPStatus.OK,
)
async def get_menu(menu_id: int, db: AsyncSession = Depends(get_db)):
    """Get one Menu and it's details from database.
    Specify the ID of Menu to get."""
    key = f"/api/v1/menus/{menu_id}"
    cached_menu = await Cache.get_from_cache(key)
    if cached_menu:
        return cached_menu
    menu = await read.get_menu_by_id(db=db, menu_id=menu_id)
    if menu:
        await Cache.set_to_cache(key, jsonable_encoder(menu))
        return menu
    raise HTTPException(status_code=404, detail="menu not found")


@router.patch(
    "/{menu_id}",
    response_model=m.Menu,
    summary="Update the menu",
    status_code=HTTPStatus.OK,
)
async def update_menu(
    menu_id: int,
    menu: m.MenuCreateUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict[str, int]:
    """Update a Menu-record in database.
    Specify the ID of the menu to be updated,
    it's new 'title' and 'description'."""
    key = f"/api/v1/menus/{menu_id}"
    upd_menu = await read.get_menu_by_id(db=db, menu_id=menu_id)
    if not upd_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    upd_menu.title = menu.title
    upd_menu.description = menu.description
    await Cache.set_to_cache(key, jsonable_encoder(upd_menu))
    await update.update_menu(
        db=db, menu_id=menu_id, new_title=menu.title, new_descr=menu.description
    )
    return upd_menu


@router.delete(
    "/{menu_id}",
    response_model=None,
    summary="Delete the menu",
    status_code=HTTPStatus.OK,
)
async def delete_menu(menu_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    """Delete a Menu.
    Specify the ID of the menu to be deleted from the database.
    Attention: Deleting a menu will result in the removal
    of all its submenus and dishes."""
    key = "/api/v1/menus"
    del_menu = await delete.delete_menu(db=db, menu_id=menu_id)
    if del_menu:
        await Cache.clear_cache(key)
        return {"status": True, "message": "The menu has been deleted"}
    raise HTTPException(status_code=404, detail="menu not found")
