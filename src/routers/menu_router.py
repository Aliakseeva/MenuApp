from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from src.database import get_db
from ..schemas import menu_schemas as m
from ..crud import delete, read, create, update


router = APIRouter(tags=['Menus'], prefix='/api/v1/menus')


@router.get('/', response_model=List[m.Menu])
def get_all_menus(db: Session = Depends(get_db)):
    """Gets a list of menu"""

    menus_l = read.get_menus(db=db)
    return menus_l


@router.get('/{menu_id}', response_model=m.Menu)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """Gets certain menu by id"""

    menu = read.get_menu_by_id(db=db, menu_id=menu_id)
    if menu:
        return menu
    else:
        raise HTTPException(status_code=404, detail='menu not found')


@router.post('/', response_model=m.Menu, status_code=201)
def create_menu(menu: m.MenuCreateUpdate, db: Session = Depends(get_db)):
    """Creates a new menu"""

    new_menu = create.create_menu(db=db, menu=menu)
    return new_menu


@router.patch('/{menu_id}', response_model=m.Menu)
def update_menu(menu_id: int, menu: m.MenuCreateUpdate, db: Session = Depends(get_db)):
    """Updates the menu"""

    upd_menu = read.get_menu_by_id(db=db, menu_id=menu_id)
    if not upd_menu:
        raise HTTPException(status_code=404, detail='menu not found')
    else:
        upd_menu.title = menu.title
        upd_menu.description = menu.description
        return update.update_menu(db=db, menu_id=menu_id)


@router.delete('/{menu_id}', response_model=None)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """Deletes the menu"""

    del_menu = delete.delete_menu(db=db, menu_id=menu_id)
    if del_menu:
        return {'status': True, 'message': 'The menu has been deleted'}
