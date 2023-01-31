from sqlalchemy.orm import Session

from .read import get_dish_by_id, get_menu_by_id, get_submenu_by_id


def update_menu(db: Session, menu_id: int):
    """Update the menu record in database.

        Parameters:
            db: Session object,
            menu_id: ID of which menu to update.

        Returns:
            upd_menu: The updated menu record.
    """
    db.commit()
    upd_menu = get_menu_by_id(db=db, menu_id=menu_id)
    return upd_menu


def update_submenu(db: Session, submenu_id: int):
    """Update the submenu record in database.

        Parameters:
            db: Session object,
            submenu_id: ID of which submenu to update.

        Returns:
            upd_submenu: The updated menu record.
    """
    db.commit()
    upd_submenu = get_submenu_by_id(db=db, submenu_id=submenu_id)
    return upd_submenu


def update_dish(db: Session, dish_id: int):
    """Update the dish record in database.

        Parameters:
            db: Session object,
            dish_id: ID of which dish to update.

        Returns:
            upd_dish: The updated dish record.
    """
    db.commit()
    upd_dish = get_dish_by_id(db=db, dish_id=dish_id)
    return upd_dish
