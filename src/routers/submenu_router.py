from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.src.database import get_db
from ..schemas import submenu_schemas as sm
from ..crud import delete, read, create, update


router = APIRouter(tags=['Submenus'], prefix='/api/v1/menus/{menu_id}/submenus')


@router.post('/', response_model=sm.Submenu, status_code=201)
def create_submenu(menu_id: int, submenu: sm.SubmenuCreateUpdate, db: Session = Depends(get_db)):
    """Creates a new submenu"""

    new_submenu = create.create_submenu(db=db, submenu=submenu, menu_id=menu_id)
    return new_submenu


@router.get('/', response_model=List[sm.Submenu])
def read_all_submenus(menu_id: int, db: Session = Depends(get_db)):
    """Gets a list of submenus"""

    submenus_l = read.get_submenus(db=db, menu_id=menu_id)
    return submenus_l


@router.get('/{submenu_id}', response_model=sm.Submenu)
def read_submenu(submenu_id: int, db: Session = Depends(get_db)):
    """Gets the submenu"""

    submenu = read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if submenu:
        return submenu
    else:
        raise HTTPException(status_code=404, detail='submenu not found')


@router.patch('/{submenu_id}', response_model=sm.Submenu)
def update_submenu(submenu_id: int, submenu: sm.SubmenuCreateUpdate, db: Session = Depends(get_db)):
    """Updates the submenu"""

    upd_submenu = read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if not upd_submenu:
        raise HTTPException(status_code=404, detail='submenu not found')
    else:
        upd_submenu.title = submenu.title
        upd_submenu.description = submenu.description
        return update.update_submenu(db=db, submenu_id=submenu_id)


@router.delete('/{submenu_id}', response_model=None)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Deletes the submenu """

    del_submenu = delete.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if del_submenu:
        return {'status': True, 'message': 'The menu has been deleted'}
