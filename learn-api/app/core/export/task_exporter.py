import re
from io import BytesIO
from typing import List, Type

import requests
from app.core.config import settings
from app.core.export.export_helper import ExportHelper
from app.crud.crud_base_task import crud_base_task
from app.crud.crud_task_group import crud_task_group
from app.crud.crud_user import crud_user
from app.crud.crud_user_solution import crud_user_solution
from app.models.task import Task
from app.schemas.base_task import BaseTask, BaseTaskDetail
from app.schemas.polygon_data import AnnotationData, AnnotationType
from app.schemas.task import TaskType
from app.schemas.task_group import TaskGroup
from app.schemas.user import User
from app.schemas.user_solution import UserSolution
from pydantic import BaseModel, parse_obj_as
from sqlalchemy.orm import Session
from xlsxwriter.worksheet import Worksheet


class TaskPointRow(BaseModel):
    user_id: int
    first_name: str
    middle_name: str
    last_name: str
    x: float
    y: float
    label: str
    question: str
    task_name: str
    task_group_name: str
    image: str


class TaskExporter:
    @staticmethod
    def write_xlsx_header(worksheet: Worksheet, model: Type[BaseModel]) -> None:
        """
        Writes all fields in the given model to the worksheet first row

        :param worksheet: Worksheet to write to
        :param model: Model which field represent the column names
        """
        char = "A"
        for index, field in enumerate(model.__fields__):
            col = chr(ord(char[0]) + index) + "1"
            worksheet.write(col, field)

    @staticmethod
    def export_point_task_group_as_xlsx(db: Session, task_group: TaskGroup) -> BytesIO:
        """
        Creates worksheet of point user solutions to the given task group

        :param db: DB-Session
        :param task_group: The task group to export the points from
        :return: Bytes representation of the worksheet
        """
        workbook, worksheet, output = ExportHelper.initialize_xlsx_file()
        ExportHelper.write_xlsx_header(worksheet, TaskPointRow)

        start_row = 2

        for base_task in task_group.tasks:
            try:
                image = requests.get(
                    settings.SLIDE_URL + "/slides/" + base_task.slide_id + "/name"
                ).json()["name"]
            except Exception as e:
                print(e)
                image = {"name": "Not Found"}
            start_row = TaskExporter.write_rows_for_base_task(
                db, worksheet, base_task, task_group, image, start_row
            )

        workbook.close()
        output.seek(0)
        return output

    @staticmethod
    def export_point_base_task_as_xlsx(
        db: Session, base_task: BaseTaskDetail, task_group=None
    ) -> BytesIO:
        """
        Creates worksheet of point user solutions to the given base task

        :param db: DB-Session
        :param base_task: The base task to export the points from
        :param task_group: The task group of the base task
        :return: Bytes representation of the worksheet
        """
        if not task_group:
            task_group = crud_task_group.get(db, id=base_task.task_group_id)

        workbook, worksheet, output = ExportHelper.initialize_xlsx_file()

        try:
            image = requests.get(
                settings.SLIDE_URL + "/slides/" + base_task.slide_id + "/name"
            ).json()["name"]
        except Exception as e:
            print(e)
            image = {"name": "Not Found"}

        ExportHelper.write_xlsx_header(worksheet, TaskPointRow)

        start_row = 2
        for task in base_task.tasks:
            user_solutions = crud_user_solution.get_solution_to_task(
                db, task_id=task.id
            )
            start_row += TaskExporter.write_rows_for_task(
                db,
                worksheet,
                user_solutions,
                task,
                base_task,
                task_group,
                image,
                start_row,
            )

        workbook.close()
        output.seek(0)
        return output

    @staticmethod
    def export_point_task_as_xlsx(
        db: Session,
        task: Task,
        base_task: BaseTask = None,
        task_group: TaskGroup = None,
    ) -> BytesIO:
        """
        Creates worksheet of point user solutions to the given task

        :param db: DB-Session
        :param task: The task to export the points from
        :param base_task: The base task of the task
        :param task_group: The task group of the task
        :return: Bytes representation of the worksheet
        """
        if not base_task:
            base_task = crud_base_task.get(db, id=task.base_task_id)
        if not task_group:
            task_group = crud_task_group.get(db, id=base_task.task_group_id)

        try:
            image = requests.get(
                settings.SLIDE_URL + "/slides/" + base_task.slide_id + "/name"
            ).json()["name"]
        except Exception as e:
            print(e)
            image = {"name": "Not Found"}

        user_solutions = crud_user_solution.get_solution_to_task(db, task_id=task.id)

        workbook, worksheet, output = ExportHelper.initialize_xlsx_file()

        ExportHelper.write_xlsx_header(worksheet, TaskPointRow)

        TaskExporter.write_rows_for_task(
            db,
            worksheet,
            user_solutions,
            task,
            base_task,
            task_group,
            image,
            start_row=2,
        )

        workbook.close()
        output.seek(0)

        return output

    @staticmethod
    def write_rows_for_task(
        db: Session,
        worksheet: Worksheet,
        user_solutions: List[UserSolution],
        task: Task,
        base_task: BaseTask,
        task_group: TaskGroup,
        image: str,
        start_row: int,
    ) -> int:
        """
        Writes one row for each user solution

        :param db: DB-Session
        :param worksheet: Worksheet to write to
        :param user_solutions: User solutions to extract data from
        :param task: The task of the user solutions
        :param base_task: The base task of the user solutions
        :param task_group: The task group of the user solutions
        :param image: Image path of the task
        :param start_row: Where to start writing
        :return: The last row written to
        """
        char = "A"
        row_num = 0
        for user_solution in user_solutions:
            user = crud_user.get(db, id=user_solution.user_id)
            user_solution_rows = TaskExporter.get_point_row(
                user_solution, user, task, base_task, task_group, image
            )

            for index, row in enumerate(user_solution_rows):
                for col_index, item in enumerate(TaskPointRow.__fields__):
                    json_row = row.dict()
                    worksheet.write(
                        chr(ord(char[0]) + col_index) + str(start_row + row_num),
                        json_row[item],
                    )
                row_num += 1

        return row_num

    @staticmethod
    def write_rows_for_base_task(
        db: Session,
        worksheet: Worksheet,
        base_task: BaseTaskDetail,
        task_group: TaskGroup,
        image: str,
        start_row: int,
    ) -> int:
        """
        Writes rows for each task in base task

        :param db: DB-Session
        :param worksheet: The worksheet to write to
        :param base_task: The base task to extract data from
        :param task_group: The task group of the base task
        :param image: The image of the base task
        :param start_row: Where to start writing
        :return: The last row written to
        """
        for task in base_task.tasks:
            user_solutions = crud_user_solution.get_solution_to_task(
                db, task_id=task.id
            )
            start_row += TaskExporter.write_rows_for_task(
                db,
                worksheet,
                user_solutions,
                task,
                base_task,
                task_group,
                image,
                start_row,
            )

        return start_row

    @staticmethod
    def get_point_row(
        user_solution: UserSolution,
        user: User,
        task: Task,
        base_task: BaseTask,
        task_group: TaskGroup,
        image: str,
    ) -> List[TaskPointRow]:
        """
        Converts each annotation of the given user solution to an object representing a row in the worksheet

        :param user_solution: User solution that should be converted
        :param user: User of the user solution
        :param task: Task of the user solution
        :param base_task: Base task of the user solution
        :param task_group: Task group of the user solution
        :param image: Image of the base task
        :return: All Row objects
        """
        task_point_rows = []

        if (
            task.annotation_type == AnnotationType.SOLUTION_POINT
            and task.task_type != TaskType.IMAGE_SELECT
        ):
            parsed_data = parse_obj_as(
                List[AnnotationData], user_solution.solution_data
            )
            for annotation in parsed_data:

                label = annotation.name
                if not annotation.name:
                    found_bracket_text = re.findall("\((.*?)\)", task.task_question)
                    if len(found_bracket_text) > 0:
                        label = found_bracket_text[0]
                    else:
                        label = ""
                task_point_rows.append(
                    TaskPointRow(
                        user_id=user.id,
                        first_name=user.firstname,
                        middle_name=user.middlename or "",
                        last_name=user.lastname,
                        x=annotation.coord.image[0].x,
                        y=annotation.coord.image[0].y,
                        label=label,
                        question=task.task_question,
                        task_name=base_task.name,
                        task_group_name=task_group.name,
                        image=image,
                    )
                )

        return task_point_rows
