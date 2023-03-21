from dataclasses import dataclass
from http import HTTPStatus

import pandas as pd

from MenuApp.src.services.tasks.cel import celery
from MenuApp.src.services.tasks.report_service import ReportService


@celery.task
def to_exel(data):
    """Generate a xlsx-file from given data.

    Parameters:
        data: a dict-template to write in xlsx-file,

    Returns:
        None.
    """
    task_id = celery.current_task.request.id
    df = pd.DataFrame(data)
    df.to_excel(f"./reports/{task_id}.xlsx")
    return task_id


@dataclass
class TaskService:
    report: ReportService

    async def generate_report_from_data(self):
        """Start a task to generate report.
        Can be downloaded later with get-request."""

        data = await self.report.get_data()
        formatted_data = self.report.formate_data(report_data=data)

        task_id = to_exel.delay(formatted_data)
        return {"task ID": task_id.__str__(), "status": HTTPStatus.ACCEPTED}
