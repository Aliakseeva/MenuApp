from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.services.crud.read import (
    get_dish_by_id,
    get_menu_by_id,
    get_submenu_by_id,
)


async def delete_menu(db: AsyncSession, menu_id: int) -> bool:
    """Delete the menu record in database.

    Parameters:
        db: AsyncSession object,
        menu_id: ID of which menu to delete.

    Returns:
        True: If deleted successfully,
        False: If any error occurred.
    """
    del_menu = await get_menu_by_id(db, menu_id)
    if del_menu:
        await db.delete(del_menu)
        await db.commit()
        return True
    return False


async def delete_submenu(db: AsyncSession, menu_id: int, submenu_id: int) -> bool:
    """Delete the submenu record in database.

    Parameters:
        db: AsyncSession object,
        menu_id: Which menu ID the submenu belongs to.
        submenu_id: ID of which submenu to delete.

    Returns:
        True: If deleted successfully,
        False: If any error occurred.
    """
    del_submenu = await get_submenu_by_id(db, submenu_id)
    if del_submenu:
        db_menu = await get_menu_by_id(db=db, menu_id=menu_id)
        db_menu.submenus_count -= 1
        db_menu.dishes_count -= del_submenu.dishes_count
        await db.delete(del_submenu)
        await db.commit()
        return True
    return False


async def delete_dish(db: AsyncSession, dish_id: int, menu_id: int, submenu_id: int) -> bool:
    """Delete the dish record in database.

    Parameters:
        db: AsyncSession object,
        menu_id: Which menu ID the dish belongs to.
        submenu_id: Which submenu ID the dish belongs to.
        dish_id: ID of which dish to delete.

    Returns:
        True: If deleted successfully,
        False: If any error occurred.
    """
    del_dish = await get_dish_by_id(db, dish_id)
    await db.delete(del_dish)
    await db.commit()
    if del_dish:
        menu = await get_menu_by_id(db=db, menu_id=menu_id)
        menu.dishes_count -= 1

        submenu = await get_submenu_by_id(db=db, submenu_id=submenu_id)
        submenu.dishes_count -= 1

        return True
    return False
