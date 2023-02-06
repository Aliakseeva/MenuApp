from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.services.crud import create
from MenuApp.src.services.data import (
    DISH_EXAMPLE_1_1,
    DISH_EXAMPLE_1_2,
    MENU_EXAMPLE,
    SUBMENU_EXAMPLE_1,
    SUBMENU_EXAMPLE_2,
)


async def create_example(db: AsyncSession):
    for menu in MENU_EXAMPLE:
        menu_ex = await create.create_menu(db=db, example=menu)
        for submenu in SUBMENU_EXAMPLE_1:
            submenu_ex = await create.create_submenu(
                db=db, example=submenu, menu_id=menu_ex.id
            )
            for dish in DISH_EXAMPLE_1_1:
                await create.create_dish(
                    db=db, example=dish, menu_id=menu_ex.id, submenu_id=submenu_ex.id
                )
        for submenu in SUBMENU_EXAMPLE_2:
            submenu_ex = await create.create_submenu(
                db=db, example=submenu, menu_id=menu_ex.id
            )
            for dish in DISH_EXAMPLE_1_2:
                await create.create_dish(
                    db=db, example=dish, menu_id=menu_ex.id, submenu_id=submenu_ex.id
                )
