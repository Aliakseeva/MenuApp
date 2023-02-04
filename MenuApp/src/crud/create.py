from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Dish, Menu, Submenu
from ..schemas import dish_schemas as d
from ..schemas import menu_schemas as m
from ..schemas import submenu_schemas as sm
from .read import get_menu_by_id, get_submenu_by_id


async def create_menu(db: AsyncSession, menu: m.MenuCreateUpdate):
    """Create new menu record in database.

    Parameters:
        db: AsyncSession object,
        menu: Validation Schema,

    Returns:
        db_menu: The created menu record.
    """
    db_menu = Menu(**menu.dict())
    db.add(db_menu)
    await db.commit()
    return db_menu


async def create_submenu(
    db: AsyncSession, submenu: sm.SubmenuCreateUpdate, menu_id: int
):
    """Create new submenu record in database.

    Parameters:
        db: AsyncSession object,
        submenu: Validation Schema,
        menu_id: Which menu ID the submenu belongs to.

    Returns:
        db_submenu: The created submenu record.
    """
    db_submenu = Submenu(**submenu.dict())
    db_submenu.menu_id = menu_id

    menu = await get_menu_by_id(db=db, menu_id=menu_id)
    menu.submenus_count += 1

    db.add(db_submenu)
    await db.commit()
    return db_submenu


async def create_dish(
    db: AsyncSession, dish: d.DishCreateUpdate, menu_id: int, submenu_id: int
):
    """Create new dish record in database.

    Parameters:
        db: AsyncSession object,
        dish: Validation Schema,
        menu_id: Which menu ID the dish belongs to.
        submenu_id: Which submenu ID the dish belongs to.

    Returns:
        db_dish: The created dish record.
    """
    db_dish = Dish(**dish.dict())
    db_dish.submenu_id = submenu_id

    menu = await get_menu_by_id(db=db, menu_id=menu_id)
    menu.dishes_count += 1

    submenu = await get_submenu_by_id(db=db, submenu_id=submenu_id)
    submenu.dishes_count += 1

    db.add(db_dish)
    await db.commit()
    return db_dish
