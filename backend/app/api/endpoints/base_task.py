import datetime
import json
import os
import traceback
import uuid
from io import StringIO
from typing import Any, Dict, List

import pandas as pd
import pyvips
import requests
from app.api.deps import (check_if_user_can_access_course,
                          get_current_active_superuser,
                          get_current_active_user, get_db)
from app.core.config import settings
from app.core.export.task_exporter import TaskExporter
from app.core.solver.solver import Solver
from app.crud.crud_base_task import crud_base_task
from app.crud.crud_course import crud_course
from app.crud.crud_task import crud_task
from app.crud.crud_task_group import crud_task_group
from app.crud.crud_task_hint import crud_task_hint
from app.crud.crud_task_statistic import crud_task_statistic
from app.crud.crud_user_solution import crud_user_solution
from app.models.user import User
from app.schemas.base_task import (BaseTask, BaseTaskCreate, BaseTaskDetail,
                                   BaseTaskUpdate)
from app.schemas.membersolution_summary import (MembersolutionSummary,
                                                SummaryRow, SummaryUser)
from app.schemas.statistic import (ImageSelectStatistic, WrongImageStatistic,
                                   WrongLabelDetailStatistic,
                                   WrongLabelStatistic)
from app.schemas.task import (TaskAnnotationType, TaskCreate, TaskStatus,
                              TaskType)
from app.schemas.task_hint import TaskHint
from app.schemas.task_statistic import TaskStatisticCreate
from app.schemas.user_solution import (UserSolution, UserSolutionCreate,
                                       UserSolutionUpdate)
from app.utils.colored_printer import ColoredPrinter
from app.utils.minio_client import MinioClient, minio_client
from app.utils.timer import Timer
from fastapi import APIRouter, Depends, HTTPException
from fastapi.datastructures import UploadFile
from fastapi.params import File, Form
from pydantic.tools import parse_obj_as
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

router = APIRouter()


@router.post('', response_model=BaseTask)
def create_base_task(*, db: Session = Depends(get_db), base_task_in: BaseTaskCreate,
                     current_user: User = Depends(get_current_active_superuser)) -> Any:
    duplicate_base_task = crud_base_task.get_by_name(db, name=base_task_in.name,
                                                     task_group_id=base_task_in.task_group_id)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=base_task_in.course_id)

    if duplicate_base_task:
        raise HTTPException(
            status_code=400,
            detail="BaseTask name already exists"
        )

    base_task = crud_base_task.create(db, obj_in=base_task_in)
    return base_task


@router.post('/imageselect/csv')
def create_base_task_from_csv(*, db: Session = Depends(get_db), base_task_in: str = Form(...),
                              csv_file: UploadFile = File(...),
                              image_dicts: str = Form(...)) -> Any:
    base_task_in = parse_obj_as(BaseTaskCreate, json.loads(base_task_in))
    image_dicts = json.loads(image_dicts)

    duplicate_base_task = crud_base_task.get_by_name(db, name=base_task_in.name,
                                                     task_group_id=base_task_in.task_group_id)
    if duplicate_base_task:
        if image_dicts:
            for image in image_dicts:
                minio_client.bucket_name = MinioClient.task_bucket
                minio_client.delete_object(image["task_image_id"])

        raise HTTPException(
            status_code=400,
            detail="BaseTask name already exists"
        )

    base_task = crud_base_task.create(db, obj_in=base_task_in)

    tasks = []

    try:
        tab = pd.read_csv(StringIO(str(csv_file.file.read(), 'utf-8')), nrows=1, sep='\t').shape[1]
        csv_file.file.seek(0)
        com = pd.read_csv(StringIO(str(csv_file.file.read(), 'utf-8')), nrows=1, sep=';').shape[1]
        csv_file.file.seek(0)
        if tab > com:
            df = pd.read_csv(StringIO(str(csv_file.file.read(), 'utf-8')), sep='\t')
        else:
            df = pd.read_csv(StringIO(str(csv_file.file.read(), 'utf-8')), sep=';')

        divider_options = [9, 12]

        labels = df['class'].unique()
        index = 0
        curr_divider = divider_options[0]
        task_index = 0

        label_update_dict = []

        for i in range(0, len(df.index)):
            if index == curr_divider or i == len(df.index) - 1:
                task_label = labels[task_index % len(labels)]
                sub_df = df[i - curr_divider:i].copy()
                image_names = sub_df['name'].unique()
                replace = {}
                for name in image_names:
                    path = [image for image in image_dicts if image['name'] == name]
                    path_item = None
                    if len(path) > 0:
                        path_item = path[0]["task_image_id"]
                        if path_item:
                            replace[name] = path_item
                        label_update_dict.append({"task_image_id": path[0]["task_image_id"],
                                                  "label": sub_df[sub_df["name"] == name]["class"].values[0]})
                    else:
                        sub_df = sub_df[sub_df["name"] != name]

                sub_df.replace({"name": replace}, inplace=True)
                correct_rows = sub_df.loc[df['class'] == task_label]['name'].to_list()
                task_create = TaskCreate(
                    layer=1,
                    base_task_id=base_task.id,
                    task_type=TaskType.IMAGE_SELECT,
                    task_question=str(task_label),
                    knowledge_level=0,
                    min_correct=0,
                    annotation_type=TaskAnnotationType.POINT,
                    solution=json.loads(json.dumps(correct_rows)),
                    task_data=sub_df['name'].to_list()
                )
                tasks.append(crud_task.create(db, obj_in=task_create))

                curr_divider = divider_options[index % len(divider_options)]
                index = 0
                task_index += 1
            else:
                index += 1
        db.refresh(base_task)
        base_task.task_count = len(tasks)
        response = requests.put(settings.SLIDE_URL + '/task-images', json=label_update_dict)
        return base_task

    except Exception as e:
        print(e)
        if image_dicts:
            for image in image_dicts:
                minio_client.bucket_name = MinioClient.task_bucket
                minio_client.delete_object(image["task_image_id"])
        if tasks:
            for task in tasks:
                if task.id:
                    crud_task.remove(db, model_id=task.id)
        if base_task and base_task.id:
            crud_base_task.remove(db, model_id=base_task.id)

        raise HTTPException(
            status_code=500,
            detail="BaseTask could not be created"
        )


@router.put('', response_model=BaseTask)
def update_base_task(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser),
                     obj_in: BaseTaskUpdate) -> BaseTask:
    base_task = crud_base_task.get(db, id=obj_in.base_task_id)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=base_task.course_id)

    duplicate_base_task = crud_base_task.get_by_name(db, name=obj_in.name, task_group_id=base_task.task_group_id)

    if duplicate_base_task:
        raise HTTPException(
            status_code=400,
            detail="BaseTask name already exists"
        )

    base_task = crud_base_task.update(db, db_obj=base_task, obj_in=obj_in)
    return base_task


@router.get('/{short_name}', response_model=BaseTaskDetail)
def read_task_details(*, db: Session = Depends(get_db), short_name: str,
                      current_user: User = Depends(get_current_active_user)) -> Any:
    base_task = crud_base_task.get_by_short_name(db, short_name=short_name)

    if crud_course.is_not_member_and_owner(db, course_id=base_task.course_id, user_id=current_user.id):
        course = crud_course.get(db, id=base_task.course_id)
        raise HTTPException(
            status_code=403,
            detail={"course": {"name": course.name, "short_name": course.short_name, "owner": {
                "firstname": course.owner.firstname,
                "lastname": course.owner.lastname
            }}}
        )
    crud_task.remove_new_task(db, base_task_id=base_task.id, user_id=current_user.id)

    for task in base_task.tasks:
        task.user_solution = crud_user_solution.get_solution_to_task_and_user(db, task_id=task.id,
                                                                              user_id=current_user.id)
        delattr(task, 'solution')

    task_group = crud_task_group.get(db=db, id=base_task.task_group_id)
    base_task.task_group_short_name = task_group.short_name

    return base_task


@router.get('/{short_name}/admin', response_model=BaseTaskDetail)
def read_task_details_admin(*, db: Session = Depends(get_db), short_name: str,
                            current_user: User = Depends(get_current_active_superuser)) -> Any:
    base_task = crud_base_task.get_by_short_name(db, short_name=short_name)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=base_task.course_id)

    for task in base_task.tasks:
        task.user_solution = crud_user_solution.get_solution_to_task_and_user(db, task_id=task.id,
                                                                              user_id=current_user.id)

    task_group = crud_task_group.get(db=db, id=base_task.task_group_id)
    base_task.task_group_short_name = task_group.short_name

    return base_task


@router.get('/{short_name}/userSolution/download', response_model=Any, response_description='xlsx')
def download_usersolutions(*, db: Session = Depends(get_db), short_name: str,
                           current_user: User = Depends(get_current_active_superuser)) -> Any:
    base_task = crud_base_task.get_by_short_name(db, short_name=short_name)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=base_task.course_id)

    output = TaskExporter.export_point_base_task_as_xlsx(db, base_task)

    headers = {
        'Content-Disposition': 'attachment; filename="' + base_task.short_name + '"'
    }

    return StreamingResponse(output, headers=headers)


@router.delete('/{short_name}', response_model=BaseTask)
def delete_base_task(*, db: Session = Depends(get_db), short_name: str,
                     current_user: User = Depends(get_current_active_user)) -> Any:
    base_task = crud_base_task.get_by_short_name(db, short_name=short_name)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=base_task.course_id)

    crud_task.remove_all_to_task_id(db, base_task_id=base_task.id)
    crud_user_solution.remove_all_to_base_task(db, base_task_id=base_task.id)
    crud_task_statistic.remove_all_by_base_task_id(db, base_task_id=base_task.id)

    for task in base_task.tasks:
        if task.task_type == TaskType.IMAGE_SELECT:
            for image in task.task_data:
                minio_client.bucket_name = MinioClient.task_bucket
                minio_client.delete_object(image)

    crud_base_task.remove(db, model_id=base_task.id)
    return base_task


@router.get('/noGroup', response_model=List[BaseTask])
def get_base_tasks_with_no_group(*, db: Session = Depends(get_db), course_id: int,
                                 current_user: User = Depends(get_current_active_user)) -> Any:
    base_tasks = crud_base_task.get_multi_with_no_task_group(db, course_id=course_id)
    return base_tasks


@router.get('/{short_name}/membersolutionsummary', response_model=MembersolutionSummary)
def get_membersolution_summary(*, db: Session = Depends(get_db), short_name: str,
                               current_user: User = Depends(get_current_active_superuser)) -> Any:
    base_task = crud_base_task.get_by_short_name(db, short_name=short_name)

    check_if_user_can_access_course(db, current_user.id, base_task.course_id)

    course = crud_course.get(db, id=base_task.course_id)

    summary = MembersolutionSummary()
    summary.tasks = []
    summary.rows = []
    for task in base_task.tasks:
        summary.tasks.append(task.task_question)

    members = sorted(course.members, key=lambda x: x.lastname)
    for member in members:
        row = SummaryRow()
        row.user = SummaryUser()
        row.user.firstname = member.firstname
        row.user.middlename = member.middlename
        row.user.lastname = member.lastname
        row.summary = []
        for task in base_task.tasks:
            user_solution = crud_user_solution.get_solution_to_task_and_user(db, user_id=member.id, task_id=task.id)
            if user_solution:
                row.summary.append(1 if user_solution.percentage_solved == 1.0 else -1)
            else:
                row.summary.append(0)
        summary.rows.append(row)

    return summary


@router.post('/userSolution', response_model=UserSolution)
def save_user_solution(*, db: Session = Depends(get_db), user_solution_in: UserSolutionCreate,
                       current_user: User = Depends(get_current_active_user)) -> Any:
    user_solution = crud_user_solution.get_solution_to_task_and_user(db, user_id=current_user.id,
                                                                     task_id=user_solution_in.task_id)

    user_solution_in.user_id = current_user.id

    if user_solution is not None:
        user_solution_in.solution_data = []
        crud_user_solution.update(db, db_obj=user_solution, obj_in=UserSolutionUpdate(**user_solution_in.dict()))

    else:
        user_solution_in.user_id = current_user.id
        if user_solution_in.course_id is None:
            base_task = crud_base_task.get(db, id=user_solution_in.base_task_id)
            user_solution_in.course_id = base_task.course_id
        user_solution_in.task_result = None
        user_solution_in.solution_data = json.loads(user_solution_in.solution_data)
        user_solution = crud_user_solution.create(db, obj_in=user_solution_in)
    return user_solution


@router.delete('/{task_id}/userSolution', response_model=UserSolution)
def remove_user_solution(*, db: Session = Depends(get_db), task_id: int,
                         current_user: User = Depends(get_current_active_user)) -> UserSolution:
    return crud_user_solution.remove_by_user_id_and_task_id(db=db, user_id=current_user.id, task_id=task_id)


@router.put('/{task_id}/userSolution', response_model=UserSolution)
def update_user_solution(*, db: Session = Depends(get_db), task_id: int, user_solution_in: UserSolutionUpdate,
                         current_user: User = Depends(get_current_active_user)) -> Any:
    user_solution_in.user_id = current_user.id
    user_solution_in.solution_data = json.loads(user_solution_in.solution_data)
    # if len(user_solution_in.solution_data) == 0:
    #     item = crud_user_solution.remove_by_user_id_and_task_id(db, user_id=current_user.id,
    #                                                             task_id=task_id)
    #     item.solution_data = user_solution_in.solution_data
    #     return item
    db_obj = crud_user_solution.get_solution_to_task_and_user(db, task_id=task_id,
                                                              user_id=current_user.id)
    solution = crud_user_solution.update(db, db_obj=db_obj, obj_in=user_solution_in)

    return solution


@router.get('/{task_id}/solve', response_model=Any)
def solve_task(*, db: Session = Depends(get_db), task_id: int, current_user: User = Depends(get_current_active_user)):
    timer = Timer()
    timer.start()
    task = crud_task.get(db, id=task_id)
    user_solution = crud_user_solution.get_solution_to_task_and_user(db, task_id=task_id, user_id=current_user.id)
    if not user_solution:
        return None
    task_result = Solver.solve(user_solution=user_solution.solution_data, task=task)
    solution_update = UserSolutionUpdate(task_result=task_result)
    if task_result.task_status == TaskStatus.CORRECT:
        solution_update.percentage_solved = 1.0
    else:
        crud_user_solution.increment_failed_attempts(db, user_id=current_user.id, task_id=task_id)
        solution_update.percentage_solved = 0.0

    crud_user_solution.update(db, db_obj=user_solution, obj_in=solution_update)

    crud_task_statistic.create(db, obj_in=TaskStatisticCreate(
        user_id=current_user.id,
        task_id=task.id,
        base_task_id=user_solution.base_task_id,
        solved_date=datetime.datetime.now(),
        percentage_solved=solution_update.percentage_solved,
        solution_data=user_solution.solution_data,
        task_result=task_result
    ))

    timer.stop()
    ColoredPrinter.print_lined_info(f"Completet in {timer.total_run_time * 1000}ms")
    return task_result


@router.post('/hint/{hint_id}/image', response_model=Dict)
def upload_task_hint_image(*, db: Session = Depends(get_db), hint_id: int,
                           current_user: User = Depends(get_current_active_superuser),
                           image: UploadFile = File(...)) -> Any:
    image_name = uuid.uuid4()

    file_name = f"{image_name}.{image.filename.split('.')[-1]}"

    final_name = f'{image_name}.jpeg'

    pyvips_image = pyvips.Image.new_from_buffer(image.file.read(), options="")

    pyvips_image.jpegsave(final_name, Q=75)

    try:
        minio_client.bucket_name = MinioClient.hint_bucket
        minio_client.create_object(file_name, final_name, "image/jpeg")
        os.remove(final_name)
        return {"path": minio_client.bucket_name + '/' + file_name}
    except Exception as e:
        print(e)
        os.remove(final_name)
        raise HTTPException(
            status_code=500,
            detail="Image could not be saved"
        )


@router.delete('/hint/{hint_id}', response_model=TaskHint)
def remove_task_hint(*, db: Session = Depends(get_db), hint_id: int,
                     current_user: User = Depends(get_current_active_superuser)):
    return crud_task_hint.remove(db, model_id=hint_id)


@router.get("/hints/{task_id}", response_model=List[TaskHint])
def get_task_hints(*, db: Session = Depends(get_db), task_id: int,
                   current_user: User = Depends(get_current_active_user)):
    failed_attempts = 99999999

    user_solution = crud_user_solution.get_solution_to_task_and_user(db, task_id=task_id, user_id=current_user.id)

    if not current_user.is_superuser and not user_solution:
        failed_attempts = 0

    if user_solution:
        failed_attempts = user_solution.failed_attempts

    hints = crud_task_hint.get_hints_by_task(db, task_id=task_id, mistakes=failed_attempts)
    return hints


@router.get("/{short_name}/statistic", response_model=Any)
def get_statistic_to_base_task(*, db: Session = Depends(get_db), short_name: str):
    base_task = crud_base_task.get_by_short_name(db, short_name=short_name)

    task_statistics, task_ids = \
        crud_task_statistic.get_oldest_task_statistics_to_base_task_id(db, base_task_id=base_task.id)

    mapped_tasks = {}

    for task_id in task_ids:
        if task_id not in mapped_tasks:
            mapped_tasks[task_id] = crud_task.get(db, id=task_id)

    task_data = []

    for task in mapped_tasks.values():
        if task.task_data:
            task_data.extend(task.task_data)

    if len(task_data) > 0 and task.task_type == TaskType.IMAGE_SELECT:
        print(task_data)
        image_query = '&taskimageid='.join(task_data)
        loaded_images = requests.get(settings.SLIDE_URL + '/task-images?taskimageid=' + image_query).json()
    else:
        return ImageSelectStatistic(
            wrong_image_statistics=[],
            wrong_label_statistics=[]
        )
    most_wrong_picked_images = {}
    most_wrong_classified_images = {}

    for task_statistic in task_statistics:
        task = mapped_tasks[task_statistic.task_id]
        if task.task_type == TaskType.IMAGE_SELECT:
            for image_uuid in task_statistic.solution_data:
                if not image_uuid in task.solution:
                    image = next((image for image in loaded_images if image["task_image_id"] == image_uuid), None)
                    if image:
                        if image["label"]:
                            if task.task_question in most_wrong_classified_images:

                                if image["label"] in most_wrong_classified_images[task.task_question]:
                                    most_wrong_classified_images[task.task_question][image["label"]] += 1
                                else:
                                    most_wrong_classified_images[task.task_question][image["label"]] = 1
                            else:
                                most_wrong_classified_images[task.task_question] = {}
                                most_wrong_classified_images[task.task_question][image["label"]] = 1
                    if image_uuid in most_wrong_picked_images:
                        most_wrong_picked_images[image_uuid] += 1
                    else:
                        most_wrong_picked_images[image_uuid] = 1

    most_wrong_picked_images = dict(sorted(most_wrong_picked_images.items(), key=lambda elem: elem[1], reverse=True))
    most_wrong_picked_images_sorted = {key: most_wrong_picked_images[key] for key in
                                       list(most_wrong_picked_images)[0:5]}

    result_images = []
    if len(most_wrong_picked_images_sorted.keys()) > 0:
        for key in most_wrong_picked_images_sorted.keys():
            image = next((image for image in loaded_images if image["task_image_id"] == key), None)
            if image:
                result_images.append(image)
                image["amount"] = most_wrong_picked_images_sorted[image["task_image_id"]]

    for item in most_wrong_classified_images:
        most_wrong_classified_images[item] = dict(
            sorted(most_wrong_classified_images[item].items(), key=lambda elem: elem[1], reverse=True))

    most_wrong_classified_images = dict(
        sorted(most_wrong_classified_images.items(), key=lambda elem: list(elem[1].values())[0], reverse=True))

    most_wrong_classified_images = {key: most_wrong_classified_images[key] for key in
                                    list(most_wrong_classified_images)[0:5]}

    result_wrong_classified = []
    for key, value in most_wrong_classified_images.items():
        detail = []

        for detail_key, detail_value in value.items():
            detail.append(
                WrongLabelDetailStatistic(
                    label=detail_key,
                    amount=detail_value
                )
            )
        wrong_label_statistic = WrongLabelStatistic(
            label=key,
            detail=detail
        )
        result_wrong_classified.append(wrong_label_statistic)

    return ImageSelectStatistic(
        wrong_image_statistics=parse_obj_as(List[WrongImageStatistic], result_images),
        wrong_label_statistics=result_wrong_classified
    )
