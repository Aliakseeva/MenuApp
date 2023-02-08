from http import HTTPStatus

from fastapi import Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.database import get_db
from MenuApp.src.routers.custom_APIRouter import APIRouter
from MenuApp.src.services import data_example
from MenuApp.src.services.tasks.report import formate_data, get_report_data, to_exel

router = APIRouter(tags=["Additional"], prefix="/api/v1/report")


@router.post("/xlsx", summary="Generate report xlsx-file", status_code=HTTPStatus.ACCEPTED)
async def gen_report(db: AsyncSession = Depends(get_db)):
    """Start a task to generate report.
    You can download it later with get-request."""
    data = await get_report_data(db)
    formatted_data = formate_data(data)
    task_id = to_exel.delay(formatted_data)
    return {"task ID": task_id.__str__(), "status": HTTPStatus.ACCEPTED}


@router.get(
    "/xlsx",
    summary="Get link to download report xlsx-file",
    status_code=HTTPStatus.OK,
)
async def get_report():
    """Get a link to download full report, generated before."""
    return FileResponse(
        "./MenuApp/src/services/tasks/report.xlsx",
        media_type="application/excel",
        filename="report.xlsx",
    )


@router.post(
    "/example",
    summary="Fill database with example data",
    status_code=HTTPStatus.CREATED,
)
async def generate_example(db: AsyncSession = Depends(get_db)):
    """Fill database with example data."""
    await data_example.create_example(db=db)
    return {"status": HTTPStatus.OK}
