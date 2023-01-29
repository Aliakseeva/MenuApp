from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..cache import clear_cache, get_from_cache, set_to_cache
from ..crud import create, delete, read, update
from ..database import get_db
from ..schemas import dish_schemas as d

router = APIRouter(
    tags=['Dish'], prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
)


@router.post('/', response_model=d.Dish, summary='Create a new dish', status_code=HTTPStatus.CREATED)
def create_dish(
    menu_id: int,
    submenu_id: int,
    dish: d.DishCreateUpdate,
    db: Session = Depends(get_db),
):
    key = f'/api/v1/menus/{menu_id}'
    new_dish = create.create_dish(
        db=db, dish=dish, menu_id=menu_id, submenu_id=submenu_id,
    )
    if new_dish:
        clear_cache(key)
        return new_dish
    raise HTTPException(status_code=405, detail='Invalid input')


@router.get('/', response_model=List[d.Dish], summary='Get a dishes list', status_code=HTTPStatus.OK)
def get_all_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):

    key = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
    cached_l = get_from_cache(key)
    if cached_l:
        return cached_l
    dishes_l = read.get_dishes(db=db, submenu_id=submenu_id)
    set_to_cache(key, jsonable_encoder(dishes_l))
    return dishes_l


@router.get('/{dish_id}', response_model=d.Dish, summary='Get dish details', status_code=HTTPStatus.OK)
def get_dish(
    menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db),
):
    key = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    cached_dish = get_from_cache(key)
    if cached_dish:
        return cached_dish
    dish = read.get_dish_by_id(db=db, dish_id=dish_id)
    if dish:
        set_to_cache(key, jsonable_encoder(dish))
        return dish
    raise HTTPException(status_code=404, detail='dish not found')


@router.patch('/{dish_id}', response_model=d.Dish, summary='Update the dish', status_code=HTTPStatus.OK)
def update_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish: d.DishCreateUpdate,
    db: Session = Depends(get_db),
):
    key = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    upd_dish = read.get_dish_by_id(db=db, dish_id=dish_id)
    if not upd_dish:
        raise HTTPException(status_code=404, detail='dish not found')
    upd_dish.title = dish.title
    upd_dish.description = dish.description
    upd_dish.price = dish.price
    set_to_cache(key, jsonable_encoder(upd_dish))
    return update.update_dish(db=db, dish_id=dish_id)


@router.delete('/{dish_id}', response_model=None, summary='Delete the dish', status_code=HTTPStatus.OK)
def delete_dish(
    menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db),
):
    key = f'/api/v1/menus/{menu_id}'
    del_dish = delete.delete_dish(
        db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id,
    )
    if del_dish:
        clear_cache(key)
        return {'status': True, 'message': 'The dish has been deleted'}
    raise HTTPException(status_code=404, detail='dish not found')
