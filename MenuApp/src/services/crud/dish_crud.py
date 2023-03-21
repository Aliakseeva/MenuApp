from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.models import Dish
from MenuApp.src.schemas.dish_schemas import DishCreateUpdate


@dataclass
class DishCrud:
    db: AsyncSession

    async def get_by_id(self, dish_id: int):
        dish = await self.db.get(Dish, dish_id)
        return dish if dish else None

    async def get_list(self, submenu_id: int):
        stmt = select(Dish).where(Dish.submenu_id == submenu_id)
        dishes_list = await self.db.execute(stmt)
        return dishes_list.scalars().all()

    async def create(self, submenu_id: int, dish: DishCreateUpdate):
        new_dish = Dish(**dish.dict())
        new_dish.submenu_id = submenu_id

        self.db.add(new_dish)
        await self.db.commit()
        await self.db.refresh(new_dish)
        return new_dish

    async def update(self, dish_id: int, dish: DishCreateUpdate):
        upd_dish = await self.db.get(Dish, dish_id)
        upd_dish_data = dish.dict(exclude_unset=True)
        for k, v in upd_dish_data.items():
            setattr(upd_dish, k, v)
        await self.db.commit()
        await self.db.refresh(upd_dish)
        return upd_dish

    async def delete(self, dish_id: int):
        del_dish = await self.db.get(Dish, dish_id)
        if del_dish:
            await self.db.delete(del_dish)
            await self.db.commit()
            return True
        return False
