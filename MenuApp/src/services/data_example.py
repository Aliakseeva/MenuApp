from random import sample, uniform

from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.schemas.dish_schemas import DishCreateUpdate
from MenuApp.src.schemas.menu_schemas import MenuCreateUpdate
from MenuApp.src.schemas.submenu_schemas import SubmenuCreateUpdate
from MenuApp.src.services.crud import create
from MenuApp.src.services.data import DESCRIPTIONS, TITLES


async def create_example(db: AsyncSession):
    title_list = sample(TITLES, 2)
    description_list = sample(DESCRIPTIONS, 2)
    menu_id = []
    submenu_id = []

    for t, d in zip(title_list, description_list):
        menu_ex = await create.create_menu(db=db, menu=MenuCreateUpdate(title=t, description=d))
        menu_id.append(menu_ex.id)

    title_list = sample(TITLES, 3)
    description_list = sample(DESCRIPTIONS, 3)

    for m_id in menu_id:
        for t, d in zip(title_list, description_list):
            submenu_ex = await create.create_submenu(
                db=db, submenu=SubmenuCreateUpdate(title=t, description=d), menu_id=m_id
            )
            submenu_id.append(submenu_ex.id)

    title_list = sample(TITLES, 5)
    description_list = sample(DESCRIPTIONS, 5)

    for m_id in menu_id:
        for sm_id in submenu_id:
            for t, d in zip(title_list, description_list):
                await create.create_dish(
                    db=db,
                    dish=DishCreateUpdate(
                        title=t, description=d, price=round(uniform(50.50, 70000.00), 2)
                    ),
                    menu_id=m_id,
                    submenu_id=sm_id,
                )
