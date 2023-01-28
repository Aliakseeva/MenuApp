from sqlalchemy.orm import Session

from .read import get_dish_by_id, get_menu_by_id, get_submenu_by_id


def update_menu(db: Session, menu_id: int):
    db.commit()
    return get_menu_by_id(db=db, menu_id=menu_id)


def update_submenu(db: Session, submenu_id: int):
    db.commit()
    return get_submenu_by_id(db=db, submenu_id=submenu_id)


def update_dish(db: Session, dish_id: int):
    db.commit()
    return get_dish_by_id(db=db, dish_id=dish_id)
