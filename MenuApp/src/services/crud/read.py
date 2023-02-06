from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.models import Dish, Menu, Submenu


async def get_menu_by_id(db: AsyncSession, menu_id: int):
    """Get menu record from database.

    Parameters:
        db: AsyncSession object,
        menu_id: ID of which menu to get.

    Returns:
        menu: The menu record with menu_id.
    """
    stmt = select(Menu).where(Menu.id == menu_id)
    menu = await db.execute(stmt)
    return menu.scalar_one_or_none()


async def get_submenu_by_id(db: AsyncSession, submenu_id: int):
    """Get submenu record from database.

    Parameters:
        db: AsyncSession object,
        submenu_id: ID of which submenu to get.

    Returns:
        submenu: The submenu record with menu_id.
    """
    stmt = select(Submenu).where(Submenu.id == submenu_id)
    submenu = await db.execute(stmt)
    return submenu.scalar_one_or_none()


async def get_dish_by_id(db: AsyncSession, dish_id: int):
    """Get dish record from database.

    Parameters:
        db: AsyncSession object,
        dish_id: ID of which dish to get.

    Returns:
        dish: The dish record with menu_id.
    """
    stmt = select(Dish).where(Dish.id == dish_id)
    dish = await db.execute(stmt)
    return dish.scalar_one_or_none()


async def get_menus(db: AsyncSession):
    """Get a list of all menu records from database.

    Parameters:
        db: AsyncSession object.

    Returns:
        menu_list: The list of menus records with menu_id.
    """
    stmt = select(Menu)
    menu_list = await db.execute(stmt)
    return menu_list.scalars().all()


async def get_submenus(menu_id: int, db: AsyncSession):
    """Get a list of all submenu records which belong to the certain menu from database.

    Parameters:
        db: AsyncSession object,
        menu_id: Which menu ID the submenus belong to.

    Returns:
        submenu_list: The list of submenus records with menu_id.
    """
    stmt = select(Submenu)
    submenu_list = await db.execute(stmt)
    return submenu_list.scalars().all()


async def get_dishes(submenu_id: int, db: AsyncSession):
    """Get a list of all dishes records which belong to the certain submenu from database.

    Parameters:
        db: AsyncSession object,
        submenu_id: Which submenu ID the dishes belong to.

    Returns:
        dish_list: The list of submenus records with menu_id.
    """
    stmt = select(Dish)
    dish_list = await db.execute(stmt)
    return dish_list.scalars().all()
