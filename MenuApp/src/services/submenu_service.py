from dataclasses import dataclass

from fastapi import HTTPException

from .crud.submenu_crud import SubmenuCrud
from ..schemas.submenu_schemas import SubmenuCreateUpdate
from .cache_service import CacheService


@dataclass
class SubmenuService:
    crud: SubmenuCrud
    cache: CacheService

    async def get_list(self, menu_id: int):
        cached_l = await self.cache.get('submenus_list')
        if cached_l:
            return cached_l
        submenus_l = await self.crud.get_list(menu_id=menu_id)
        await self.cache.set('submenus_list', submenus_l)
        return submenus_l

    async def get_one(self, submenu_id: int):
        cached_submenu = await self.cache.get(f'submenu_{submenu_id}')
        if cached_submenu:
            return cached_submenu
        submenu = await self.crud.get_by_id(submenu_id)
        if submenu:
            await self.cache.set(f'submenu_{submenu_id}', submenu)
            return submenu
        raise HTTPException(status_code=404, detail="submenu not found")

    async def create(self, menu_id: int, submenu: SubmenuCreateUpdate):
        await self.cache.clear()
        return await self.crud.create(menu_id=menu_id, submenu=submenu)
        # raise HTTPException(status_code=405, detail="Invalid input")

    async def update(self, submenu_id: int, submenu: SubmenuCreateUpdate):
        upd_submenu = await self.crud.get_by_id(submenu_id)
        if not upd_submenu:
            raise HTTPException(status_code=404, detail="submenu not found")
        upd_submenu = await self.crud.update(submenu_id, submenu)
        await self.cache.clear()
        return upd_submenu

    async def delete(self, submenu_id: int):
        del_submenu = await self.crud.delete(submenu_id)
        if del_submenu:
            await self.cache.clear()
            return {"status": True, "message": "The submenu has been deleted"}
        raise HTTPException(status_code=404, detail="submenu not found")
