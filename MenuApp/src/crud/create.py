from sqlalchemy.orm import Session

from ..models import Dish, Menu, Submenu
from ..schemas import dish_schemas as d
from ..schemas import menu_schemas as m
from ..schemas import submenu_schemas as sm
from .read import get_menu_by_id, get_submenu_by_id


def create_menu(db: Session, menu: m.MenuCreateUpdate):
    """Create new menu record in database.

        Parameters:
            db: Session object,
            menu: Validation Schema,

        Returns:
            db_menu: The created menu record.
    """
    db_menu = Menu(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def create_submenu(db: Session, submenu: sm.SubmenuCreateUpdate, menu_id: int):
    """Create new submenu record in database.

        Parameters:
            db: Session object,
            submenu: Validation Schema,
            menu_id: Which menu ID the submenu belongs to.

        Returns:
            db_submenu: The created submenu record.
    """
    db_submenu = Submenu(**submenu.dict())
    db_submenu.menu_id = menu_id
    get_menu_by_id(db=db, menu_id=menu_id).submenus_count += 1
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def create_dish(db: Session, dish: d.DishCreateUpdate, menu_id: int, submenu_id: int):
    """Create new dish record in database.

        Parameters:
            db: Session object,
            dish: Validation Schema,
            menu_id: Which menu ID the dish belongs to.
            submenu_id: Which submenu ID the dish belongs to.

        Returns:
            db_dish: The created dish record.
    """
    db_dish = Dish(**dish.dict())
    db_dish.submenu_id = submenu_id
    get_menu_by_id(db=db, menu_id=menu_id).dishes_count += 1
    get_submenu_by_id(db=db, submenu_id=submenu_id).dishes_count += 1
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish
