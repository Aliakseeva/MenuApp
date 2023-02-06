from datetime import datetime

import pandas as pd
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from MenuApp.src.models import Menu, Submenu
from MenuApp.src.services.tasks.cel import celery


async def get_report_data(db: AsyncSession) -> list:
    """Generate a list of all menus, submenus and dishes.

    Parameters:
        db: AsyncSession object,

    Returns:
        report: a list of all menus, submenus and dishes.
    """
    stmt = select(Menu).options(joinedload(Menu.submenus).joinedload(Submenu.dishes))
    data = await db.execute(stmt)
    return jsonable_encoder(data.scalars().unique().all())


def formate_data(report_data) -> dict:
    """Generate a dict-template to write in xlsx-file.

    Parameters:
        report_data: JSON-file with all data,

    Returns:
        template: a dict-template to write in xlsx-file.
    """
    generated_date = datetime.now().strftime("%d %B %Y at %H:%M")
    description = f"Report generated {generated_date}"
    template = {
        "A": [description],
        "B": [""],
        "C": [""],
        "D": [""],
        "E": [""],
        "F": [""],
    }

    for i, menu in enumerate(report_data, 1):
        # template['A'].append(menu['id'])
        template["A"].append(str(i))
        template["B"].append(menu["title"])
        template["C"].append(menu["description"])
        template["D"].append("")
        template["E"].append("")
        template["F"].append("")

        for j, submenu in enumerate(menu["submenus"], 1):
            template["A"].append("")
            # template['B'].append(submenu['id'])
            template["B"].append(str(j))
            template["C"].append(submenu["title"])
            template["D"].append(submenu["description"])
            template["E"].append("")
            template["F"].append("")

            for k, dish in enumerate(submenu["dishes"], 1):
                template["A"].append("")
                template["B"].append("")
                # template['C'].append(dish['id'])
                template["C"].append(str(k))
                template["D"].append(dish["title"])
                template["E"].append(dish["description"])
                template["F"].append(dish["price"])

    return template


@celery.task
def to_exel(data):
    """Generate a xlsx-file from given data.

    Parameters:
        data: a dict-template to write in xlsx-file,

    Returns:
        None.
    """
    df = pd.DataFrame(data)
    df.to_excel("report.xlsx")
