from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..cache import clear_cache, get_from_cache, set_to_cache
from ..crud import create, delete, read, update
from ..database import get_db
from ..schemas import menu_schemas as m

router = APIRouter(tags=['Menus'], prefix='/api/v1/menus')


@router.get('/', response_model=List[m.Menu])
def get_all_menus(db: Session = Depends(get_db)):
    """Gets a list of menu"""

    key = '/api/v1/menus'
    cached_l = get_from_cache(router.prefix)
    if cached_l:
        return cached_l
    menus_l = read.get_menus(db=db)
    set_to_cache(key, jsonable_encoder(menus_l))
    return menus_l


@router.get('/{menu_id}', response_model=m.Menu)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """Gets certain menu by id"""

    key = f'/api/v1/menus/{menu_id}'
    cached_menu = get_from_cache(key)
    if cached_menu:
        return cached_menu
    menu = read.get_menu_by_id(db=db, menu_id=menu_id)
    if menu:
        set_to_cache(key, jsonable_encoder(menu))
        return menu
    raise HTTPException(status_code=404, detail='menu not found')


@router.post('/', response_model=m.Menu, status_code=201)
def create_menu(menu: m.MenuCreateUpdate, db: Session = Depends(get_db)):
    """Creates a new menu"""

    key = '/api/v1/menus'
    new_menu = create.create_menu(db=db, menu=menu)
    if new_menu:
        clear_cache(key)
        return new_menu


@router.patch('/{menu_id}', response_model=m.Menu)
def update_menu(menu_id: int, menu: m.MenuCreateUpdate, db: Session = Depends(get_db)):
    """Updates the menu"""

    key = f'/api/v1/menus/{menu_id}'
    upd_menu = read.get_menu_by_id(db=db, menu_id=menu_id)
    if not upd_menu:
        raise HTTPException(status_code=404, detail='menu not found')
    else:
        upd_menu.title = menu.title
        upd_menu.description = menu.description
        set_to_cache(key, jsonable_encoder(upd_menu))
        return update.update_menu(db=db, menu_id=menu_id)


@router.delete('/{menu_id}', response_model=None)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """Deletes the menu"""

    key = '/api/v1/menus'
    del_menu = delete.delete_menu(db=db, menu_id=menu_id)
    if del_menu:
        clear_cache(key)
        return {'status': True, 'message': 'The menu has been deleted'}
