from dataclasses import dataclass

from fastapi import HTTPException

from .crud.dish_crud import DishCrud
from ..schemas.dish_schemas import DishCreateUpdate
from .cache_service import CacheService


@dataclass
class DishService:
    crud: DishCrud
    cache: CacheService

    async def get_list(self, submenu_id: int):
        cached_l = await self.cache.get('dishes_list')
        if cached_l:
            return cached_l
        dishes_l = await self.crud.get_list(submenu_id=submenu_id)
        await self.cache.set('dishes_list', dishes_l)
        return dishes_l

    async def get_one(self, dish_id: int):
        cached_dish = await self.cache.get(f'dish_{dish_id}')
        if cached_dish:
            return cached_dish
        dish = await self.crud.get_by_id(dish_id)
        if dish:
            await self.cache.set(f'dish_{dish_id}', dish)
            return dish
        raise HTTPException(status_code=404, detail="dish not found")

    async def create(self, submenu_id: int, dish: DishCreateUpdate):
        await self.cache.clear()
        return await self.crud.create(submenu_id=submenu_id, dish=dish)

    async def update(self, dish_id: int, dish: DishCreateUpdate):
        upd_dish = await self.crud.get_by_id(dish_id)
        if not upd_dish:
            raise HTTPException(status_code=404, detail="submenu not found")
        upd_dish = await self.crud.update(dish_id=dish_id, dish=dish)
        await self.cache.set(f'dish_{dish_id}', upd_dish)
        await self.cache.clear()
        return upd_dish

    async def delete(self, dish_id: int):
        del_dish = await self.crud.delete(dish_id=dish_id)
        if del_dish:
            await self.cache.clear()
            return {"status": True, "message": "The dish has been deleted"}
        raise HTTPException(status_code=404, detail="dish not found")
