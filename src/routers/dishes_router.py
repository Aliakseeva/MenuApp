from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemes import dish_schemes as d
from src.crud import delete, read, create, update
from src.database import get_db


dish_router = APIRouter(prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['dishes'])


@dish_router.post('/', response_model=d.Dish, status_code=201)
def create_dish(menu_id: int, submenu_id: int, dish: d.DishCreate, db: Session = Depends(get_db)):
    """Creating a new dish"""

    return create.create_dish(db=db, dish=dish, menu_id=menu_id, submenu_id=submenu_id)


@dish_router.get('/', response_model=list[d.Dish])
def get_all_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Get a list of menus"""

    dishes_l = read.get_dishes(db=db, submenu_id=submenu_id)
    return dishes_l


@dish_router.get('/{dish_id}', response_model=d.Dish)
def get_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    """Get certain dish by id"""

    dish = read.get_dish_by_id(db=db, dish_id=dish_id)
    if dish:
        return dish


@dish_router.patch('/{dish_id}', response_model=d.Dish)
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: d.DishUpdate, db: Session = Depends(get_db)):
    """Updating certain dish by id"""

    upd_dish = read.get_dish_by_id(db=db, dish_id=dish_id)
    if upd_dish:
        upd_dish.title = dish.title
        upd_dish.description = dish.description
        upd_dish.price = dish.price
        return update.update_dish(db=db, dish_id=dish_id)


@dish_router.delete('/{dish_id}')
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    """Deleting certain dish by id"""

    del_dish = delete.delete_dish(db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id)
    if del_dish:
        return {'status': 'True', 'message': 'DELETED successfully'}
