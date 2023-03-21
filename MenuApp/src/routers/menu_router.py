from http import HTTPStatus

from fastapi import Depends
from MenuApp.src.routers.custom_APIRouter import APIRouter

from MenuApp.src.dependencies import get_menu_service
from MenuApp.src.schemas import menu_schemas
from MenuApp.src.services.menu_service import MenuService


router = APIRouter(tags=["Menu"], prefix="/api/v1/menus")


@router.get(
    "/",
    response_model=list[menu_schemas.Menu],
    summary="Get a menus list",
    status_code=HTTPStatus.OK,
)
async def get_all_menus(menu_service: MenuService = Depends(get_menu_service)):
    """Get all Menu-records and their details from database in list."""
    return await menu_service.get_list()


@router.get(
    "/{menu_id}",
    response_model=menu_schemas.Menu,
    summary="Get menu details",
    status_code=HTTPStatus.OK,
)
async def get_menu(menu_id: int, menu_service: MenuService = Depends(get_menu_service)):
    """Get one Menu and it's details from database.
    Specify the ID of Menu to get."""
    return await menu_service.get_one(menu_id=menu_id)


@router.post(
    "/",
    response_model=menu_schemas.Menu,
    summary="Create a new menu",
    status_code=HTTPStatus.CREATED,
)
async def create_menu(
    menu: menu_schemas.MenuCreateUpdate, menu_service: MenuService = Depends(get_menu_service)
):
    """Create a Menu-record in database.
    Specify the title and the description to set."""
    return await menu_service.create(menu=menu)


@router.patch(
    "/{menu_id}",
    response_model=menu_schemas.Menu,
    summary="Update the menu",
    status_code=HTTPStatus.OK,
)
async def update_menu(
    menu_id: int,
    menu: menu_schemas.MenuCreateUpdate,
    menu_service: MenuService = Depends(get_menu_service),
):
    """Update a Menu-record in database.
    Specify the ID of the menu to be updated,
    it's new 'title' and 'description'."""
    return await menu_service.update(menu_id=menu_id, menu=menu)


@router.delete(
    "/{menu_id}",
    response_model=None,
    summary="Delete the menu",
    status_code=HTTPStatus.OK,
)
async def delete_menu(menu_id: int, menu_service: MenuService = Depends(get_menu_service)):
    """Delete a Menu.
    Specify the ID of the menu to be deleted from the database.
    Attention: Deleting a menu will result in the removal
    of all its submenus and dishes."""
    return await menu_service.delete(menu_id=menu_id)
