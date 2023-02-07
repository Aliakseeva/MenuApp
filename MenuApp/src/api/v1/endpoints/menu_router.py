from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
#
# from MenuApp.src.cache import Cache
# from MenuApp.src.db import get_db
from MenuApp.src.api.v1.endpoints.custom_APIRouter import APIRouter
from MenuApp.src.db.database import get_db
from MenuApp.src.db.schemas import MenuCreateUpdate, Menu
from MenuApp.src.services.db_service import read, create, update, delete
from MenuApp.src.services.menu_service import create_menu_service, update_menu_service, list_all_menus_service, delete_menu_service, get_menu_service


router = APIRouter(tags=["Menu"], prefix="/api/v1/menus")


@router.post(
    "/",
    response_model=Menu,
    summary="Create a new menu",
    status_code=HTTPStatus.CREATED,
)
async def create_menu(menu: MenuCreateUpdate, db: AsyncSession = Depends(get_db)) -> dict[str, int]:
    """"""
    return await create_menu_service(menu=menu, db=db)


@router.get(
    "/",
    response_model=list[Menu],
    summary="Get a menus list",
    status_code=HTTPStatus.OK,
)
async def get_all_menus(db: AsyncSession = Depends(get_db)):
    return await list_all_menus_service(db=db)


@router.get(
    "/{menu_id}",
    response_model=Menu,
    summary="Get menu details",
    status_code=HTTPStatus.OK,
)
async def get_menu(menu_id: int, db: AsyncSession = Depends(get_db)):
    return await get_menu_service(db=db, menu_id=menu_id)


@router.patch(
    "/{menu_id}",
    response_model=Menu,
    summary="Update the menu",
    status_code=HTTPStatus.OK,
)
async def update_menu(
    menu_id: int,
    menu: MenuCreateUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict[str, int]:
    return await update_menu_service(db=db, menu=menu, menu_id=menu_id)


@router.delete(
    "/{menu_id}",
    response_model=None,
    summary="Delete the menu",
    status_code=HTTPStatus.OK,
)
async def delete_menu(menu_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    return await delete_menu_service(db=db, menu_id=menu_id)

