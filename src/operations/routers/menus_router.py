from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..schemes import menu_schemes as m
from ..crud import create
from ..crud import read
from ..crud import update
from ..crud import delete


menu_router = APIRouter(prefix='/api/v1/menus', tags=['menus'])


@menu_router.post('/', response_model=m.Menu, status_code=201)
def create_menu(menu: m.MenuCreate, db: Session):
    """Creating a new menu"""

    new_menu = create.create_menu(db=db, menu=menu)
    return new_menu


@menu_router.get('/', response_model=list[m.Menu])
def get_all_menus(db: Session):
    """Get a list of menus"""

    menus_l = read.get_menus(db=db)
    return menus_l


@menu_router.get('/{menu_id}', response_model=m.Menu)
def get_menu(menu_id: int, db: Session):
    """Get certain menu by id"""

    menu = read.get_menu_by_id(db=db, menu_id=menu_id)
    if menu:
        return menu


@menu_router.patch('/{menu_id}', response_model=m.Menu)
def update_menu(menu_id: int, menu: m.MenuUpdate, db: Session):
    """Updating certain menu by id"""

    upd_menu = read.get_menu_by_id(db=db, menu_id=menu_id)
    if upd_menu:
        upd_menu.title = menu.title
        upd_menu.description = menu.description
        return update.update_menu(db=db, menu_id=menu_id)


@menu_router.delete('/{menu_id}')
def delete_menu(menu_id: int, db: Session):
    """Deleting certain menu by id"""

    del_menu = delete.delete_menu(db=db, menu_id=menu_id)
    if del_menu:
        return {'status': True, 'message': 'DELETED successfully'}

