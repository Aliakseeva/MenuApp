from http import HTTPStatus
from MenuApp.src.dependencies import get_task_service, get_fill_test_data_service
from MenuApp.src.services.tasks.task_service import TaskService
from MenuApp.src.services.test_data_filling_service import TestDataService

from fastapi import Depends
from fastapi.responses import FileResponse
from MenuApp.src.routers.custom_APIRouter import APIRouter


router = APIRouter(tags=["Additional"], prefix="/api/v1/report")


@router.post(
    "/example",
    summary="Fill database with example data",
    status_code=HTTPStatus.CREATED,
)
async def generate_example(test_data_service: TestDataService = Depends(get_fill_test_data_service)):
    """Fill database with example data."""
    return await test_data_service.upload_example_data()


@router.delete(
    "/example",
    summary="Delete all database rows",
    status_code=HTTPStatus.OK,
)
async def delete_all(test_data_service: TestDataService = Depends(get_fill_test_data_service)):
    """Delete all rows in database!"""
    return await test_data_service.truncate_db()


@router.post("/xlsx", summary="Generate report xlsx-file", status_code=HTTPStatus.ACCEPTED)
async def generate_report(task_service: TaskService = Depends(get_task_service)):
    """Start a task to generate report.
    You can download it later with get-request."""
    return await task_service.generate_report_from_data()


@router.get(
    "/xlsx",
    summary="Get link to download report xlsx-file",
    status_code=HTTPStatus.OK,
)
async def get_report(task_id: str):
    """Get a link to download full report, generated before."""
    report_path = f'./reports/{task_id}.xlsx'

    return FileResponse(
        report_path,
        media_type="application/excel",
        filename=f'{task_id}.xlsx'
    )
