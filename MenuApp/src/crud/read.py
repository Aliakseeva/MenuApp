from sqlalchemy.orm import Session

from ..models import Dish, Menu, Submenu


def get_menu_by_id(db: Session, menu_id: int):
    """Get menu record from database.

        Parameters:
            db: Session object,
            menu_id: ID of which menu to get.

        Returns:
            menu: The menu record with menu_id.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    return menu


def get_submenu_by_id(db: Session, submenu_id: int):
    """Get submenu record from database.

        Parameters:
            db: Session object,
            submenu_id: ID of which submenu to get.

        Returns:
            submenu: The submenu record with menu_id.
    """
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    return submenu


def get_dish_by_id(db: Session, dish_id: int):
    """Get dish record from database.

        Parameters:
            db: Session object,
            dish_id: ID of which dish to get.

        Returns:
            dish: The dish record with menu_id.
    """
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    return dish


def get_menus(db: Session):
    """Get a list of all menu records from database.

        Parameters:
            db: Session object.

        Returns:
            menu_list: The list of menus records with menu_id.
    """
    menu_list = db.query(Menu).all()
    return menu_list


def get_submenus(menu_id: int, db: Session):
    """Get a list of all submenu records which belong to the certain menu from database.

        Parameters:
            db: Session object,
            menu_id: Which menu ID the submenus belong to.

        Returns:
            submenu_list: The list of submenus records with menu_id.
    """
    submenu_list = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
    return submenu_list


def get_dishes(submenu_id: int, db: Session):
    """Get a list of all dishes records which belong to the certain submenu from database.

        Parameters:
            db: Session object,
            submenu_id: Which submenu ID the dishes belong to.

        Returns:
            dish_list: The list of submenus records with menu_id.
    """
    dish_list = db.query(Dish).filter(Dish.submenu_id == submenu_id).all()
    return dish_list
