from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from ..cache import Cache
from ..crud import create, delete, read, update
from ..database import get_db
from ..schemas import dish_schemas as d

router = APIRouter(
    tags=["Dish"],
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
)


@router.post(
    "/",
    response_model=d.Dish,
    summary="Create a new dish",
    status_code=HTTPStatus.CREATED,
)
async def create_dish(
    menu_id: int,
    submenu_id: int,
    dish: d.DishCreateUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict[str, int]:
    key = f"/api/v1/menus/{menu_id}"
    new_dish = await create.create_dish(
        db=db,
        dish=dish,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    if new_dish:
        # Cache.clear_cache(key)
        return new_dish
    raise HTTPException(status_code=405, detail="Invalid input")


@router.get(
    "/",
    response_model=list[d.Dish],
    summary="Get a dishes list",
    status_code=HTTPStatus.OK,
)
async def get_all_dishes(
    menu_id: int,
    submenu_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, int]]:
    key = f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"
    # cached_l = Cache.get_from_cache(key)
    # if cached_l:
    #     return cached_l
    dishes_l = await read.get_dishes(db=db, submenu_id=submenu_id)
    # Cache.set_to_cache(key, jsonable_encoder(dishes_l))
    return dishes_l


@router.get(
    "/{dish_id}",
    response_model=d.Dish,
    summary="Get dish details",
    status_code=HTTPStatus.OK,
)
async def get_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, int]:
    key = f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    # cached_dish = Cache.get_from_cache(key)
    # if cached_dish:
    #     return cached_dish
    dish = await read.get_dish_by_id(db=db, dish_id=dish_id)
    if dish:
        # Cache.set_to_cache(key, jsonable_encoder(dish))
        return dish
    raise HTTPException(status_code=404, detail="dish not found")


@router.patch(
    "/{dish_id}",
    response_model=d.Dish,
    summary="Update the dish",
    status_code=HTTPStatus.OK,
)
async def update_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish: d.DishCreateUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict[str, int]:
    key = f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    upd_dish = await read.get_dish_by_id(db=db, dish_id=dish_id)
    # if not upd_dish:
    #     raise HTTPException(status_code=404, detail='dish not found')
    # upd_dish.title = dish.title
    # upd_dish.description = dish.description
    # upd_dish.price = dish.price
    # Cache.set_to_cache(key, jsonable_encoder(upd_dish))
    await update.update_dish(
        db=db,
        dish_id=dish_id,
        new_title=dish.title,
        new_descr=dish.description,
        new_price=dish.price,
    )
    return upd_dish


@router.delete(
    "/{dish_id}",
    response_model=None,
    summary="Delete the dish",
    status_code=HTTPStatus.OK,
)
async def delete_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict:
    key = f"/api/v1/menus/{menu_id}"
    del_dish = await delete.delete_dish(
        db=db,
        dish_id=dish_id,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    if del_dish:
        # Cache.clear_cache(key)
        return {"status": True, "message": "The dish has been deleted"}
    raise HTTPException(status_code=404, detail="dish not found")
