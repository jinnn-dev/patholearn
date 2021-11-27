from typing import Any, List
from app.schemas.task_group import TaskGroupUpdate

from starlette.responses import StreamingResponse

from app.api.deps import (check_if_user_can_access_course,
                          get_current_active_superuser,
                          get_current_active_user, get_db)
from app.core.export.task_exporter import TaskExporter
from app.crud.crud_course import crud_course
from app.crud.crud_task import crud_task
from app.crud.crud_task_group import crud_task_group
from app.crud.crud_user_solution import crud_user_solution
from app.models.user import User
from app.schemas.task_group import TaskGroup, TaskGroupCreate, TaskGroupDetail
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('', response_model=List[TaskGroup])
def get_task_groups_by_course(*, db: Session = Depends(get_db), course_id: int,
                              current_user: User = Depends(get_current_active_user)):
    task_groups = crud_task_group.get_multi_by_course_id(db, course_id=course_id)
    percentage_solved = 0.0
    for task_group in task_groups:
        percentage = crud_user_solution.get_solved_percentage_to_task_group(db, user_id=current_user.id,
                                                                            task_group_id=task_group.id)[0]
        task_group_length = len(task_group.tasks)
        if percentage and task_group_length:
            percentage_solved += float(percentage)
            task_group.percentage_solved = percentage / task_group_length
        else:
            task_group.percentage_solved = 0
    return task_groups


@router.post('', response_model=TaskGroup)
def create_task_group(*, db: Session = Depends(get_db), task_group_in: TaskGroupCreate,
                      current_user: User = Depends(get_current_active_superuser)):

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=task_group_in.course_id)

    task_group_duplicate = crud_task_group.get_by_name(db, name=task_group_in.name, course_id=task_group_in.course_id)
    if task_group_duplicate:
        raise HTTPException(
            status_code=400,
            detail="TaskGroup name already exists"
        )
    task_group = crud_task_group.create(db, obj_in=task_group_in)
    return task_group


@router.get('/{short_name}', response_model=TaskGroupDetail)
def get_task_group(*, db: Session = Depends(get_db), short_name: str,
                   current_user: User = Depends(get_current_active_user)) -> Any:
    task_group = crud_task_group.get_by_short_name(db, short_name=short_name)

    if crud_course.is_not_member_and_owner(db, course_id=task_group.course_id, user_id=current_user.id):
        course = crud_course.get(db, id=task_group.course_id)
        raise HTTPException(
            status_code=403,
            detail={"course": {"name": course.name, "short_name": course.short_name, "owner": {
                "firstname": course.owner.firstname,
                "lastname": course.owner.lastname
            }}}
        )

    task_group_percentage = 0.0
    task_count = 0

    new_tasks = []
    for task in task_group.tasks:
        new_task_count = 0

        if not task.enabled and not current_user.is_superuser:
            continue
        base_task_percentage = float(
            crud_user_solution.get_solved_percentage_to_base_task(
                db, user_id=current_user.id, base_task_id=task.id
            )[0] or 0.0
        )
        

        if crud_task.has_new_task(db, user_id=current_user.id, base_task_id=task.id):
            new_task_count += 1

        task_group_percentage += base_task_percentage
        task_len = len(task.tasks)
        task_count += task_len
        task.task_count = task_len
        task.new_tasks = new_task_count
       
        if task.tasks:
            task.percentage_solved = base_task_percentage / len(task.tasks)
        else:
            task.percentage_solved = 0
        task.correct_tasks = crud_user_solution.get_amount_of_correct_solutions_to_base_task(db,
                                                                                             user_id=current_user.id,
                                                                                             base_task_id=task.id)
        task.wrong_tasks = crud_user_solution.get_amount_of_wrong_solutions_to_base_task(db,
                                                                                             user_id=current_user.id,
                                                                                             base_task_id=task.id)

        del task.tasks
        new_tasks.append(task)

    if task_count != 0:
        task_group.percentage_solved = task_group_percentage / task_count
    else:
        task_group.percentage_solved = 0.0
    task_group.task_count = task_count
    task_group.tasks = new_tasks
    course = crud_course.get(db=db, id=task_group.course_id)
    task_group.course_short_name = course.short_name
    return task_group


@router.delete('/{short_name}', response_model=TaskGroup)
def remove_task_group(*, db: Session = Depends(get_db), short_name: str,
                      current_user: User = Depends(get_current_active_user)):
    task_group = crud_task_group.get_by_short_name(db, short_name=short_name)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=task_group.course_id)

    crud_user_solution.remove_all_to_task_group(db, task_group_id=task_group.id)
    deleted_task_group = crud_task_group.remove(db, model_id=task_group.id)
    return deleted_task_group


@router.get('/{short_name}/userSolution/download', response_model=Any, response_description='xlsx')
def download_usersolutions(*, db: Session = Depends(get_db), short_name: str,
                           current_user: User = Depends(get_current_active_superuser)) -> Any:
    task_group = crud_task_group.get_by_short_name(db, short_name=short_name)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=task_group.course_id)

    output = TaskExporter.export_point_task_group_as_xlsx(db, task_group)

    headers = {
        'Content-Disposition': 'attachment; filename="' + task_group.short_name + '"'
    }

    return StreamingResponse(output, headers=headers)

@router.put('', response_model=TaskGroup)
def update_task_group(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser),
                     obj_in: TaskGroupUpdate) -> TaskGroup:
    task_group = crud_task_group.get(db, id=obj_in.task_group_id)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=task_group.course_id)

    task_group = crud_task_group.update(db, db_obj=task_group, obj_in=obj_in)
    return task_group

