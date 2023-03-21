import os
from dataclasses import dataclass
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from MenuApp.src.models import Menu, Submenu


@dataclass
class ReportService:
    db: AsyncSession

    async def get_data(self) -> list:
        """Generate a list of all menus, submenus and dishes.

        Returns:
            report: a list of all menus, submenus and dishes.
        """
        stmt = select(Menu).options(joinedload(Menu.submenus).joinedload(Submenu.dishes))
        data = await self.db.execute(stmt)
        return jsonable_encoder(data.scalars().unique().all())

    @staticmethod
    def formate_data(report_data) -> dict:
        """Generate a dict-template to write in xlsx-file.

        Parameters:
            report_data: JSON-file with all data,

        Returns:
            template: a dict-template to write in xlsx-file.
        """
        generated_date = datetime.now().strftime("%d %B %Y at %H:%M")
        timezone = datetime.now().astimezone()
        description = f"Report generated {generated_date} ({timezone.tzinfo.__str__()})"
        template = {
            "A": [description],
            "B": [""],
            "C": [""],
            "D": [""],
            "E": [""],
            "F": [""],
        }

        for i, menu in enumerate(report_data, 1):
            template["A"].append(str(i))
            template["B"].append(menu["title"])
            template["C"].append(menu["description"])
            template["D"].append("")
            template["E"].append("")
            template["F"].append("")

            for j, submenu in enumerate(menu["submenus"], 1):
                template["A"].append("")
                template["B"].append(str(j))
                template["C"].append(submenu["title"])
                template["D"].append(submenu["description"])
                template["E"].append("")
                template["F"].append("")

                for k, dish in enumerate(submenu["dishes"], 1):
                    template["A"].append("")
                    template["B"].append("")
                    template["C"].append(str(k))
                    template["D"].append(dish["title"])
                    template["E"].append(dish["description"])
                    template["F"].append(dish["price"])

        return template

    @staticmethod
    def is_exist(file_path):
        return os.path.exists(file_path)
