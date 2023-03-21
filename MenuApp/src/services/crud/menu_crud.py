from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from MenuApp.src.models import Menu
from MenuApp.src.schemas.menu_schemas import MenuCreateUpdate


@dataclass
class MenuCrud:
    db: AsyncSession

    async def get_by_id(self, menu_id: int):
        menu = await self.db.get(Menu, menu_id)
        return menu if menu else None

    async def get_list(self):
        stmt = select(Menu)
        menus_list = await self.db.execute(stmt)
        return menus_list.scalars().all()

    async def create(self, menu: MenuCreateUpdate):
        new_menu = Menu(title=menu.title, description=menu.description)
        self.db.add(new_menu)
        await self.db.commit()
        await self.db.refresh(new_menu)
        return new_menu

    async def update(self, menu_id: int, menu: MenuCreateUpdate):
        upd_menu = await self.db.get(Menu, menu_id)
        upd_menu_data = menu.dict(exclude_unset=True)
        for k, v in upd_menu_data.items():
            setattr(upd_menu, k, v)
        await self.db.commit()
        await self.db.refresh(upd_menu)
        return upd_menu

    async def delete(self, menu_id: int):
        del_menu = await self.db.get(Menu, menu_id)
        if del_menu:
            await self.db.delete(del_menu)
            await self.db.commit()
            return True
        return False
