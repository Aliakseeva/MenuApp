from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.db.models import Dish, Menu, Submenu
from MenuApp.src.db.schemas import MenuCreateUpdate, DishCreateUpdate, SubmenuCreateUpdate


@dataclass
class DBService:
    model: Menu | Dish | Submenu
    db: AsyncSession

    async def list(self):
        """Get a list of all menu records from database.

        Parameters:
            db: AsyncSession object.

        Returns:
            menu_list: The list of menus records with menu_id.
        """
        stmt = select(self.model)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get(self, entity_id: str):
        """Get dish record from database.

        Parameters:
            db: AsyncSession object,
            dish_id: ID of which dish to get.

        Returns:
            dish: The dish record with menu_id.
        """
        stmt = select(self.model).where(self.model.id == entity_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
