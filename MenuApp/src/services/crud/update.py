from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.services.crud.read import (
    get_dish_by_id,
    get_menu_by_id,
    get_submenu_by_id,
)


async def update_menu(db: AsyncSession, menu_id: int, new_title: str, new_descr: str):
    """Update the menu record in database.

    Parameters:
        db: AsyncSession object,
        menu_id: ID of which menu to update,
        new_title: str with title to set,
        new_descr: str with description to set.

    Returns:
        upd_menu: The updated menu record.
    """
    upd_menu = await get_menu_by_id(db=db, menu_id=menu_id)
    upd_menu.title = new_title
    upd_menu.description = new_descr
    await db.commit()
    return upd_menu


async def update_submenu(db: AsyncSession, submenu_id: int, new_title: str, new_descr: str):
    """Update the submenu record in database.

    Parameters:
        db: AsyncSession object,
        submenu_id: ID of which submenu to update,
        new_title: str with title to set,
        new_descr: str with description to set.

    Returns:
        upd_submenu: The updated menu record.
    """
    upd_submenu = await get_submenu_by_id(db=db, submenu_id=submenu_id)
    upd_submenu.title = new_title
    upd_submenu.description = new_descr
    await db.commit()
    return upd_submenu


async def update_dish(
    db: AsyncSession, dish_id: int, new_title: str, new_descr: str, new_price: str
):
    """Update the dish record in database.

    Parameters:
        db: AsyncSession object,
        dish_id: ID of which dish to update,
        new_title: str with title to set,
        new_descr: str with description to set,
        new_price: str with price to set.

    Returns:
        upd_dish: The updated dish record.
    """
    upd_dish = await get_dish_by_id(db=db, dish_id=dish_id)
    upd_dish.title = new_title
    upd_dish.description = new_descr
    upd_dish.price = new_price
    await db.commit()
    return upd_dish
