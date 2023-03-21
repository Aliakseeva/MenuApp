from dataclasses import dataclass

from fastapi import HTTPException
import redis

from .crud.menu_crud import MenuCrud
from ..schemas.menu_schemas import MenuCreateUpdate


@dataclass
class MenuService:
    crud: MenuCrud
    cache: redis

    async def get_list(self):
        cached_l = await self.cache.get('menus_list')
        if cached_l:
            return cached_l

        menus_l = await self.crud.get_list()
        await self.cache.set('menus_list', menus_l)
        return menus_l

    async def get_one(self, menu_id: int):
        cached_menu = await self.cache.get(f'menu_{menu_id}')
        if cached_menu:
            return cached_menu
        menu = await self.crud.get_by_id(menu_id)
        if menu:
            await self.cache.set(f'menu_{menu_id}', menu)
            return menu
        raise HTTPException(status_code=404, detail="menu not found")

    async def create(self, menu: MenuCreateUpdate):
        await self.cache.clear()
        return await self.crud.create(menu)

    async def update(self, menu_id: int, menu: MenuCreateUpdate):
        upd_menu = await self.crud.get_by_id(menu_id)
        if not upd_menu:
            raise HTTPException(status_code=404, detail="menu not found")
        upd_menu = await self.crud.update(menu_id, menu)
        await self.cache.set(f'menu_{menu_id}', upd_menu)
        await self.cache.clear()
        return upd_menu

    async def delete(self, menu_id: int):
        del_menu = await self.crud.delete(menu_id)
        if del_menu:
            await self.cache.clear()
            return {"status": True, "message": "The menu has been deleted"}
        raise HTTPException(status_code=404, detail="menu not found")
