from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.db.models import Dish, Menu, Submenu
from MenuApp.src.db.schemas import Menu, MenuCreateUpdate, SubmenuCreateUpdate, DishCreateUpdate
from MenuApp.src.services.db_service.read import get_menu_by_id, get_submenu_by_id


async def create_menu(
    db: AsyncSession, menu: MenuCreateUpdate = None, example: dict = None
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
    else:
        db_menu = Menu(**menu.dict())
    db.add(db_menu)
    await db.commit()
    return db_menu


async def create_submenu(
    db: AsyncSession,
    menu_id: int,
    submenu: SubmenuCreateUpdate = None,
    example: dict = None,
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
    else:
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
    dish: DishCreateUpdate = None,
    example: dict = None,
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
    else:
        db_dish = Dish(**dish.dict())
    db_dish.submenu_id = submenu_id

    menu = await get_menu_by_id(db=db, menu_id=menu_id)
    menu.dishes_count += 1

    submenu = await get_submenu_by_id(db=db, submenu_id=submenu_id)
    submenu.dishes_count += 1

    db.add(db_dish)
    await db.commit()
    return db_dish
