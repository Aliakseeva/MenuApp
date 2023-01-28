from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..cache import clear_cache, get_from_cache, set_to_cache
from ..crud import create, delete, read, update
from ..database import get_db
from ..schemas import submenu_schemas as sm

router = APIRouter(
    tags=['Submenus'],
    prefix='/api/v1/menus/{menu_id}/submenus',
)


@router.post('/', response_model=sm.Submenu, status_code=201)
def create_submenu(
    menu_id: int, submenu: sm.SubmenuCreateUpdate, db: Session = Depends(get_db),
):
    """Creates a new submenu"""

    key = f'/api/v1/menus/{menu_id}'
    new_submenu = create.create_submenu(
        db=db, submenu=submenu, menu_id=menu_id,
    )
    if new_submenu:
        clear_cache(key)
        return new_submenu


@router.get('/', response_model=List[sm.Submenu])
def read_all_submenus(menu_id: int, db: Session = Depends(get_db)):
    """Gets a list of submenus"""

    key = f'/api/v1/menus/{menu_id}/submenus'
    cached_l = get_from_cache(key)
    if cached_l:
        return cached_l
    submenus_l = read.get_submenus(db=db, menu_id=menu_id)
    set_to_cache(key, jsonable_encoder(submenus_l))
    return submenus_l


@router.get('/{submenu_id}', response_model=sm.Submenu)
def read_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Gets the submenu"""

    key = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}'
    cached_submenu = get_from_cache(key)
    if cached_submenu:
        return cached_submenu
    submenu = read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if submenu:
        set_to_cache(key, jsonable_encoder(submenu))
        return submenu
    raise HTTPException(status_code=404, detail='submenu not found')


@router.patch('/{submenu_id}', response_model=sm.Submenu)
def update_submenu(
    menu_id: int,
    submenu_id: int,
    submenu: sm.SubmenuCreateUpdate,
    db: Session = Depends(get_db),
):
    """Updates the submenu"""

    key = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}'
    upd_submenu = read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if not upd_submenu:
        raise HTTPException(status_code=404, detail='submenu not found')

    upd_submenu.title = submenu.title
    upd_submenu.description = submenu.description
    set_to_cache(key, jsonable_encoder(upd_submenu))
    return update.update_submenu(db=db, submenu_id=submenu_id)


@router.delete('/{submenu_id}', response_model=None)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Deletes the submenu"""

    key = f'/api/v1/menus/{menu_id}'
    del_submenu = delete.delete_submenu(
        db=db, menu_id=menu_id, submenu_id=submenu_id,
    )
    if del_submenu:
        clear_cache(key)
        return {'status': True, 'message': 'The submenu has been deleted'}
