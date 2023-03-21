from http import HTTPStatus

from fastapi import Depends

from MenuApp.src.dependencies import get_submenu_service
from MenuApp.src.schemas import submenu_schemas
from MenuApp.src.services.submenu_service import SubmenuService

from .custom_APIRouter import APIRouter

router = APIRouter(
    tags=["Submenu"],
    prefix="/api/v1/menus/{menu_id}/submenus",
)


@router.get(
    "/",
    response_model=list[submenu_schemas.Submenu],
    summary="Get a submenus list",
    status_code=HTTPStatus.OK,
)
async def get_all_submenus(
    menu_id: int, submenu_service: SubmenuService = Depends(get_submenu_service)
):
    return await submenu_service.get_list(menu_id=menu_id)


@router.get(
    "/{submenu_id}",
    response_model=submenu_schemas.Submenu,
    summary="Get submenu details",
    status_code=HTTPStatus.OK,
)
async def get_submenu(
    submenu_id: int,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.get_one(submenu_id=submenu_id)


@router.post(
    "/",
    response_model=submenu_schemas.Submenu,
    summary="Create a new submenu",
    status_code=HTTPStatus.CREATED,
)
async def create_submenu(
    menu_id: int,
    submenu: submenu_schemas.SubmenuCreateUpdate,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.create(menu_id=menu_id, submenu=submenu)


@router.patch(
    "/{submenu_id}",
    response_model=submenu_schemas.Submenu,
    summary="Update the submenu",
    status_code=HTTPStatus.OK,
)
async def update_submenu(
    submenu_id: int,
    submenu: submenu_schemas.SubmenuCreateUpdate,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> dict[str, int]:
    return await submenu_service.update(submenu_id=submenu_id, submenu=submenu)


@router.delete(
    "/{submenu_id}",
    response_model=None,
    summary="Delete the submenu",
    status_code=HTTPStatus.OK,
)
async def delete_submenu(
    submenu_id: int,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> dict:
    return await submenu_service.delete(submenu_id=submenu_id)
