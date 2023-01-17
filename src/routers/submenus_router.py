from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from src.schemes import submenu_schemes as sm
from src.crud import delete, read, create, update
from src.database import get_db


submenu_router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=['submenus'])


@submenu_router.post('/', response_model=sm.Submenu, status_code=201)
def create_submenu(menu_id: int, submenu: sm.SubmenuCreate, db: Session = Depends(get_db)):
    """Creating a new submenu"""

    new_submenu = create.create_submenu(db=db, submenu=submenu, menu_id=menu_id)
    return new_submenu


@submenu_router.get('/', response_model=list[sm.Submenu])
def read_all_submenus(menu_id: int, db: Session = Depends(get_db)):
    """Get a list of submenus"""

    submenus_l = read.get_submenus(db=db, menu_id=menu_id)
    return submenus_l


@submenu_router.get('/{submenu_id}', response_model=sm.Submenu)
def read_submenu(submenu_id: int, db: Session = Depends(get_db)):
    """Get certain submenu by id"""

    submenu = read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if submenu:
        return submenu


@submenu_router.patch('/{submenu_id}', response_model=sm.Submenu)
def update_submenu(submenu_id: int, submenu: sm.SubmenuUpdate, db: Session = Depends(get_db)):
    """Updating certain submenu by id"""

    upd_submenu = read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if upd_submenu:
        upd_submenu.title = submenu.title
        upd_submenu.description = submenu.description
        return update.update_submenu(db=db, submenu_id=submenu_id)


@submenu_router.delete('/{submenu_id}')
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    del_submenu = delete.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if del_submenu:
        return {'status': 'True', 'message': 'DELETED successfully'}
