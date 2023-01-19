from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from src.database import get_db
from ..schemas import dish_schemas as d
from ..crud import delete, read, create, update


router = APIRouter(tags=['Dishes'], prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')


@router.post('/', response_model=d.Dish, status_code=201)
def create_dish(menu_id: int, submenu_id: int, dish: d.DishCreateUpdate, db: Session = Depends(get_db)):
    """Creating a new dish"""

    return create.create_dish(db=db, dish=dish, menu_id=menu_id, submenu_id=submenu_id)


@router.get('/', response_model=List[d.Dish])
def get_all_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Gets a list of menus"""

    dishes_l = read.get_dishes(db=db, submenu_id=submenu_id)
    return dishes_l


@router.get('/{dish_id}', response_model=d.Dish)
def get_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    """Gets certain dish by id"""

    dish = read.get_dish_by_id(db=db, dish_id=dish_id)
    if dish:
        return dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


@router.patch('/{dish_id}', response_model=d.Dish)
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: d.DishCreateUpdate, db: Session = Depends(get_db)):
    """Updating the dish by id"""

    upd_dish = read.get_dish_by_id(db=db, dish_id=dish_id)

    if not upd_dish:
        raise HTTPException(status_code=404, detail='dish not found')
    else:
        upd_dish.title = dish.title
        upd_dish.description = dish.description
        upd_dish.price = dish.price
        return update.update_dish(db=db, dish_id=dish_id)


@router.delete('/{dish_id}', response_model=None)
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    """Deletes the dish by id"""

    del_dish = delete.delete_dish(db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id)
    if del_dish:
        return {'status': True, 'message': 'The dish has been deleted'}
