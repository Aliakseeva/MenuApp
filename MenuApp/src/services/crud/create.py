from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.models import Dish, Menu, Submenu
from MenuApp.src.schemas import dish_schemas as d
from MenuApp.src.schemas import menu_schemas as m
from MenuApp.src.schemas import submenu_schemas as sm
from MenuApp.src.services.crud.read import get_menu_by_id, get_submenu_by_id


async def create_menu(
    db: AsyncSession, menu: m.MenuCreateUpdate | None = None, example: dict | None = None
):
    """Create new menu record in database.

    Parameters:
        db: AsyncSession object,
        menu: Validation Schema,
        example: Menu data for database filling.

    Returns:
        db_menu: The created menu record.
    """
    if example:
        db_menu = Menu(**example)
    elif menu:
        db_menu = Menu(**menu.dict())
    db.add(db_menu)
    await db.commit()
    return db_menu


async def create_submenu(
    db: AsyncSession,
    menu_id: int,
    submenu: sm.SubmenuCreateUpdate | None = None,
    example: dict | None = None,
):
    """Create new submenu record in database.

    Parameters:
        db: AsyncSession object,
        submenu: Validation Schema,
        menu_id: Which menu ID the submenu belongs to,
        example: Submenu data for database filling.

    Returns:
        db_submenu: The created submenu record.
    """
    if example:
        db_submenu = Submenu(**example)
    elif submenu:
        db_submenu = Submenu(**submenu.dict())
    db_submenu.menu_id = menu_id

    menu = await get_menu_by_id(db=db, menu_id=menu_id)
    menu.submenus_count += 1

    db.add(db_submenu)
    await db.commit()
    return db_submenu


async def create_dish(
    db: AsyncSession,
    menu_id: int,
    submenu_id: int,
    dish: d.DishCreateUpdate | None = None,
    example: dict | None = None,
):
    """Create new dish record in database.

    Parameters:
        db: AsyncSession object,
        dish: Validation Schema,
        menu_id: Which menu ID the dish belongs to.
        submenu_id: Which submenu ID the dish belongs to,
        example: Dish data for database filling.

    Returns:
        db_dish: The created dish record.
    """
    if example:
        db_dish = Dish(**example)
    elif dish:
        db_dish = Dish(**dish.dict())
    db_dish.submenu_id = submenu_id

    menu = await get_menu_by_id(db=db, menu_id=menu_id)
    menu.dishes_count += 1

    submenu = await get_submenu_by_id(db=db, submenu_id=submenu_id)
    submenu.dishes_count += 1

    db.add(db_dish)
    await db.commit()
    return db_dish
