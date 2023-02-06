from http import HTTPStatus

from fastapi import Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from MenuApp.src.database import get_db
from MenuApp.src.routers.custom_APIRouter import APIRouter
from MenuApp.src.services import data_example
from MenuApp.src.services.tasks.report import formate_data, get_report_data, to_exel

router = APIRouter(tags=["Additional"], prefix="/api/v1/report")


@router.post(
    "/xlsx", summary="Generate report xlsx-file", status_code=HTTPStatus.ACCEPTED
)
async def gen_report(db: AsyncSession = Depends(get_db)):
    data = await get_report_data(db)
    formatted_data = formate_data(data)
    task_id = to_exel.delay(formatted_data)
    return {"task ID": task_id.__str__()}


@router.get(
    "/xlsx",
    summary="Get link to download report xlsx-file",
    status_code=HTTPStatus.OK,
)
async def get_report():
    return FileResponse(
        "report.xlsx", media_type="application/octet-stream", filename="report.xlsx"
    )


@router.post(
    "/example",
    summary="Fill database with example data",
    status_code=HTTPStatus.CREATED,
)
async def generate_example(db: AsyncSession = Depends(get_db)):
    await data_example.create_example(db=db)
    return "Done!"
