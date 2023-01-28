from sqlalchemy.orm import Session

from .read import get_dish_by_id, get_menu_by_id, get_submenu_by_id


def delete_menu(db: Session, menu_id: int):
    del_menu = get_menu_by_id(db, menu_id)
    if del_menu:
        db.delete(del_menu)
        db.commit()
        return True


def delete_submenu(db: Session, menu_id: int, submenu_id: int):
    del_submenu = get_submenu_by_id(db, submenu_id)
    if del_submenu:
        db_menu = get_menu_by_id(db=db, menu_id=menu_id)
        db_menu.submenus_count -= 1
        db_menu.dishes_count -= del_submenu.dishes_count
        db.delete(del_submenu)
        db.commit()
        return True


def delete_dish(db: Session, dish_id: int, menu_id: int, submenu_id: int):
    del_dish = get_dish_by_id(db, dish_id)
    if del_dish:
        get_menu_by_id(db=db, menu_id=menu_id).dishes_count -= 1
        get_submenu_by_id(db=db, submenu_id=submenu_id).dishes_count -= 1
        db.delete(del_dish)
        db.commit()
        return True
