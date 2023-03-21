from http import HTTPStatus

from fastapi import Depends

from MenuApp.src.dependencies import get_dish_service
from MenuApp.src.routers.custom_APIRouter import APIRouter
from MenuApp.src.schemas import dish_schemas
from MenuApp.src.services.dish_service import DishService

router = APIRouter(
    tags=["Dish"],
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
)


@router.post(
    "/",
    response_model=dish_schemas.Dish,
    summary="Create a new dish",
    status_code=HTTPStatus.CREATED,
)
async def create_dish(
    submenu_id: int,
    dish: dish_schemas.DishCreateUpdate,
    dish_service: DishService = Depends(get_dish_service),
) -> dict[str, int]:
    return await dish_service.create(submenu_id=submenu_id, dish=dish)


@router.get(
    "/",
    response_model=list[dish_schemas.Dish],
    summary="Get a dishes list",
    status_code=HTTPStatus.OK,
)
async def get_all_dishes(
    submenu_id: int,
    dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.get_list(submenu_id=submenu_id)


@router.get(
    "/{dish_id}",
    response_model=dish_schemas.Dish,
    summary="Get dish details",
    status_code=HTTPStatus.OK,
)
async def get_dish(
    submenu_id: int,
    dish_id: int,
    dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.get_one(dish_id=dish_id)


@router.patch(
    "/{dish_id}",
    response_model=dish_schemas.Dish,
    summary="Update the dish",
    status_code=HTTPStatus.OK,
)
async def update_dish(
    dish_id: int,
    dish: dish_schemas.DishCreateUpdate,
    dish_service: DishService = Depends(get_dish_service),
) -> dict[str, int]:
    return await dish_service.update(dish_id=dish_id, dish=dish)


@router.delete(
    "/{dish_id}",
    response_model=None,
    summary="Delete the dish",
    status_code=HTTPStatus.OK,
)
async def delete_dish(
    dish_id: int,
    dish_service: DishService = Depends(get_dish_service),
) -> dict:
    return await dish_service.delete(dish_id=dish_id)
