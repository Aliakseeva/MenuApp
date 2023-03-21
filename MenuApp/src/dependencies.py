from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .database import get_redis
from .services.crud.dish_crud import DishCrud
from .services.crud.menu_crud import MenuCrud
from .services.crud.submenu_crud import SubmenuCrud
from .services.cache_service import CacheService
from .services.dish_service import DishService
from .services.menu_service import MenuService
from .services.submenu_service import SubmenuService
from .services.tasks.report_service import ReportService
from .services.tasks.task_service import TaskService
from .services.test_data_filling_service import TestDataService


async def get_cache(cache=Depends(get_redis)):
    return CacheService(cache)


async def get_menu_crud(db: AsyncSession = Depends(get_db)):
    return MenuCrud(db)


async def get_menu_service(
    crud: MenuCrud = Depends(get_menu_crud),
    cache: CacheService = Depends(get_cache),
):
    return MenuService(crud, cache)


async def _get_submenu_crud(db: AsyncSession = Depends(get_db)):
    return SubmenuCrud(db)


async def get_submenu_service(
    crud: SubmenuCrud = Depends(_get_submenu_crud),
    cache: CacheService = Depends(get_cache),
):
    return SubmenuService(crud, cache)


async def _get_dish_crud(db: AsyncSession = Depends(get_db)):
    return DishCrud(db)


async def get_dish_service(
    crud: DishCrud = Depends(_get_dish_crud),
    cache: CacheService = Depends(get_cache),
):
    return DishService(crud, cache=cache)


async def get_fill_test_data_service(db: AsyncSession = Depends(get_db), cache: CacheService = Depends(get_cache)):
    return TestDataService(db, cache)


async def _get_report_service(db: AsyncSession = Depends(get_db)):
    return ReportService(db=db)


async def get_task_service(report: ReportService = Depends(_get_report_service)):
    return TaskService(report=report)
