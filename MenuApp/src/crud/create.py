from sqlalchemy.orm import Session
from .read import get_menu_by_id, get_submenu_by_id

from ..schemas import menu_schemas as m, submenu_schemas as sm, dish_schemas as d
from MenuApp.src.models import Menu, Submenu, Dish


def create_menu(db: Session, menu: m.MenuCreateUpdate):
    db_menu = Menu(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def create_submenu(db: Session, submenu: sm.SubmenuCreateUpdate, menu_id: int):
    db_submenu = Submenu(**submenu.dict())
    db_submenu.menu_id = menu_id
    get_menu_by_id(db=db, menu_id=menu_id).submenus_count += 1
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def create_dish(db: Session, dish: d.DishCreateUpdate, menu_id: int, submenu_id: int):
    db_dish = Dish(**dish.dict())
    db_dish.submenu_id = submenu_id
    get_menu_by_id(db=db, menu_id=menu_id).dishes_count += 1
    get_submenu_by_id(db=db, submenu_id=submenu_id).dishes_count += 1
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish
