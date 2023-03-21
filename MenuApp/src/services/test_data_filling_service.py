import json
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.models import Menu, Submenu, Dish
from MenuApp.src.services.cache_service import CacheService


@dataclass
class TestDataService:
    db: AsyncSession
    cache: CacheService

    async def truncate_db(self):
        await self.cache.clear()
        instance = await self.db.execute(select(Menu))
        for i in instance.scalars().all():
            await self.db.delete(i)
            await self.db.commit()
        return {'message': 'Success!'}

    async def upload_example_data(self):
        with open('data_example.json') as data:
            data = json.load(data)

            for menu_id in data['menus']:
                menu_ex = Menu(
                    id=int(menu_id),
                    title=data['menus'][menu_id]['title'],
                    description=data['menus'][menu_id]['description']
                )
                self.db.add(menu_ex)
                await self.db.commit()
                await self.db.refresh(menu_ex)

            for submenu_id in data['submenus']:
                submenu_ex = Submenu(
                    id=int(submenu_id),
                    title=data['submenus'][submenu_id]['title'],
                    description=data['submenus'][submenu_id]['description'],
                    menu_id=data['submenus'][submenu_id]['menu_id']
                )

                self.db.add(submenu_ex)
                await self.db.commit()
                await self.db.refresh(submenu_ex)

            for dish_id in data['dishes']:
                dish_ex = Dish(
                    id=int(dish_id),
                    title=data['dishes'][dish_id]['title'],
                    description=data['dishes'][dish_id]['description'],
                    price=data['dishes'][dish_id]['price'],
                    submenu_id=data['dishes'][dish_id]['submenu_id']
                )

                self.db.add(dish_ex)
                await self.db.commit()
                await self.db.refresh(dish_ex)

        return {'message': 'Success!'}
