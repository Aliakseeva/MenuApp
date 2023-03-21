from http import HTTPStatus

from fastapi import Depends
from fastapi.responses import FileResponse

from MenuApp.src.dependencies import (
    get_fill_test_data_service,
    get_report_service,
    get_task_service,
)
from MenuApp.src.routers.custom_APIRouter import APIRouter
from MenuApp.src.services.tasks.report_service import ReportService
from MenuApp.src.services.tasks.task_service import TaskService
from MenuApp.src.services.test_data_filling_service import TestDataService

router = APIRouter(tags=["Additional"], prefix="/api/v1/report")


@router.post(
    "/example",
    summary="Fill database with example data",
    status_code=HTTPStatus.CREATED,
)
async def generate_example(
    test_data_service: TestDataService = Depends(get_fill_test_data_service),
):
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
async def get_report(task_id: str, report_service: ReportService = Depends(get_report_service)):
    """Get a link to download full report, generated before."""
    report_path = f"./reports/{task_id}.xlsx"
    if report_service.is_exist(report_path):
        return FileResponse(
            report_path, media_type="application/excel", filename=f"{task_id}.xlsx"
        )
    else:
        return {"error": "File not found"}
