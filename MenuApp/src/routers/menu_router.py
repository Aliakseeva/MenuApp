from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from ..cache import Cache
from ..crud import create, delete, read, update
from ..database import get_db
from ..schemas import menu_schemas as m

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
    key = "/api/v1/menus"
    new_menu = await create.create_menu(db=db, menu=menu)
    if new_menu:
        # Cache.clear_cache(key)
        return new_menu
    raise HTTPException(status_code=405, detail="Invalid input")


@router.get(
    "/",
    response_model=list[m.Menu],
    summary="Get a menus list",
    status_code=HTTPStatus.OK,
)
async def get_all_menus(db: AsyncSession = Depends(get_db)) -> list[dict[str, int]]:
    key = "/api/v1/menus"
    # cached_l = Cache.get_from_cache(router.prefix)
    # if cached_l:
    #     return cached_l
    menus_l = await read.get_menus(db=db)
    # Cache.set_to_cache(key, jsonable_encoder(menus_l))
    return menus_l


@router.get(
    "/{menu_id}",
    response_model=m.Menu,
    summary="Get menu details",
    status_code=HTTPStatus.OK,
)
async def get_menu(menu_id: int, db: AsyncSession = Depends(get_db)) -> dict[str, int]:
    # key = f'/api/v1/menus/{menu_id}'
    # cached_menu = Cache.get_from_cache(key)
    # if cached_menu:
    #     return cached_menu
    menu = await read.get_menu_by_id(db=db, menu_id=menu_id)
    if menu:
        # Cache.set_to_cache(key, jsonable_encoder(menu))
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
    key = f"/api/v1/menus/{menu_id}"
    upd_menu = await read.get_menu_by_id(db=db, menu_id=menu_id)
    if not upd_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    # upd_menu.title = menu.title
    # upd_menu.description = menu.description
    # Cache.set_to_cache(key, jsonable_encoder(upd_menu))
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
    key = "/api/v1/menus"
    del_menu = await delete.delete_menu(db=db, menu_id=menu_id)
    if del_menu:
        # Cache.clear_cache(key)
        return {"status": True, "message": "The menu has been deleted"}
    raise HTTPException(status_code=404, detail="menu not found")
