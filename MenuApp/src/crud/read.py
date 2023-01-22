from sqlalchemy.orm import Session
from ..models import Menu, Submenu, Dish


def get_menu_by_id(db: Session, menu_id: int):
    return db.query(Menu).filter(Menu.id == menu_id).first()


def get_submenu_by_id(db: Session, submenu_id: int):
    return db.query(Submenu).filter(Submenu.id == submenu_id).first()


def get_dish_by_id(db: Session, dish_id: int):
    return db.query(Dish).filter(Dish.id == dish_id).first()


def get_menus(db: Session):
    return db.query(Menu).all()


def get_submenus(menu_id: int, db: Session):
    return db.query(Submenu).filter(Submenu.menu_id == menu_id).all()


def get_dishes(submenu_id: int, db: Session):
    return db.query(Dish).filter(Dish.submenu_id == submenu_id).all()
