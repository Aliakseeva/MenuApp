from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.models import Submenu
from MenuApp.src.schemas.submenu_schemas import SubmenuCreateUpdate


@dataclass
class SubmenuCrud:
    db: AsyncSession

    async def get_by_id(self, submenu_id: int):
        submenu = await self.db.get(Submenu, submenu_id)
        return submenu if submenu else None

    async def get_list(self, menu_id: int):
        stmt = select(Submenu).where(Submenu.menu_id == menu_id)
        submenus_list = await self.db.execute(stmt)
        return submenus_list.scalars().all()

    async def create(self, menu_id: int, submenu: SubmenuCreateUpdate):
        new_submenu = Submenu(**submenu.dict())
        new_submenu.menu_id = menu_id

        self.db.add(new_submenu)
        await self.db.commit()
        await self.db.refresh(new_submenu)
        return new_submenu

    async def update(self, submenu_id: int, submenu: SubmenuCreateUpdate):
        upd_submenu = await self.db.get(Submenu, submenu_id)
        upd_submenu_data = submenu.dict(exclude_unset=True)
        for k, v in upd_submenu_data.items():
            setattr(upd_submenu, k, v)
        await self.db.commit()
        await self.db.refresh(upd_submenu)
        return upd_submenu

    async def delete(self, submenu_id: int):
        del_submenu = await self.db.get(Submenu, submenu_id)
        if del_submenu:
            await self.db.delete(del_submenu)
            await self.db.commit()
            return True
        return False
