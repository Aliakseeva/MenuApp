from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from ..cache import Cache
from ..crud import create, delete, read, update
from ..database import get_db
from ..schemas import submenu_schemas as sm

router = APIRouter(
    tags=["Submenu"],
    prefix="/api/v1/menus/{menu_id}/submenus",
)


@router.post(
    "/",
    response_model=sm.Submenu,
    summary="Create a new submenu",
    status_code=HTTPStatus.CREATED,
)
async def create_submenu(
    menu_id: int,
    submenu: sm.SubmenuCreateUpdate,
    db: AsyncSession = Depends(get_db),
):
    key = f"/api/v1/menus/{menu_id}"
    new_submenu = await create.create_submenu(
        db=db,
        submenu=submenu,
        menu_id=menu_id,
    )
    if new_submenu:
        # Cache.clear_cache(key)
        return new_submenu
    raise HTTPException(status_code=405, detail="Invalid input")


@router.get(
    "/",
    response_model=list[sm.Submenu],
    summary="Get a submenus list",
    status_code=HTTPStatus.OK,
)
async def read_all_submenus(
    menu_id: int, db: AsyncSession = Depends(get_db)
) -> list[dict[str, int]]:
    key = f"/api/v1/menus/{menu_id}/submenus"
    # cached_l = Cache.get_from_cache(key)
    # if cached_l:
    #     return cached_l
    submenus_l = await read.get_submenus(db=db, menu_id=menu_id)
    # Cache.set_to_cache(key, jsonable_encoder(submenus_l))
    return submenus_l


@router.get(
    "/{submenu_id}",
    response_model=sm.Submenu,
    summary="Get submenu details",
    status_code=HTTPStatus.OK,
)
async def read_submenu(
    menu_id: int,
    submenu_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, int]:
    key = f"/api/v1/menus/{menu_id}/submenus/{submenu_id}"
    # cached_submenu = Cache.get_from_cache(key)
    # if cached_submenu:
    #     return cached_submenu
    submenu = await read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if submenu:
        # Cache.set_to_cache(key, jsonable_encoder(submenu))
        return submenu
    raise HTTPException(status_code=404, detail="submenu not found")


@router.patch(
    "/{submenu_id}",
    response_model=sm.Submenu,
    summary="Update the submenu",
    status_code=HTTPStatus.OK,
)
async def update_submenu(
    menu_id: int,
    submenu_id: int,
    submenu: sm.SubmenuCreateUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict[str, int]:
    key = f"/api/v1/menus/{menu_id}/submenus/{submenu_id}"
    upd_submenu = await read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if not upd_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    # upd_submenu.title = submenu.title
    # upd_submenu.description = submenu.description
    # Cache.set_to_cache(key, jsonable_encoder(upd_submenu))
    await update.update_submenu(
        db=db,
        submenu_id=submenu_id,
        new_title=submenu.title,
        new_descr=submenu.description,
    )
    return upd_submenu


@router.delete(
    "/{submenu_id}",
    response_model=None,
    summary="Delete the submenu",
    status_code=HTTPStatus.OK,
)
async def delete_submenu(
    menu_id: int,
    submenu_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict:
    key = f"/api/v1/menus/{menu_id}"
    del_submenu = await delete.delete_submenu(
        db=db,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    if del_submenu:
        # Cache.clear_cache(key)
        return {"status": True, "message": "The submenu has been deleted"}
    raise HTTPException(status_code=404, detail="submenu not found")
