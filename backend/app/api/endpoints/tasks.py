import json
import uuid
from typing import Any, Dict, List, Union

from app.api.deps import (check_if_user_can_access_course,
                          check_if_user_can_access_task,
                          get_current_active_superuser,
                          get_current_active_user, get_db)
from app.core.solver.solver import Solver
from app.crud.crud_base_task import crud_base_task
from app.crud.crud_course import crud_course
from app.crud.crud_task import crud_task
from app.crud.crud_task_group import crud_task_group
from app.crud.crud_task_hint import crud_task_hint
from app.crud.crud_user_solution import crud_user_solution
from app.models.user import User
from app.schemas.base_task import (BaseTask, BaseTaskCreate, BaseTaskDetail,
                                   BaseTaskUpdate)
from app.schemas.polygon_data import (AnnotationData, AnnotationType,
                                      OffsetLineData, OffsetPointData,
                                      OffsetPolygonData)
from app.schemas.task import (AnnotationGroup, AnnotationGroupUpdate, Task,
                              TaskCreate, TaskFeedback, TaskStatus, TaskUpdate)
from app.schemas.task_hint import (HintType, TaskHint, TaskHintCreate,
                                   TaskHintUpdate)
from app.schemas.user_solution import (UserSolution, UserSolutionCreate,
                                       UserSolutionUpdate)
from app.utils.colored_printer import ColoredPrinter
from app.utils.minio_client import minio_client
from app.utils.timer import Timer
from fastapi import APIRouter, Depends, HTTPException
from fastapi.datastructures import UploadFile
from fastapi.params import File
from sqlalchemy.orm import Session

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


@router.put('', response_model=BaseTask)
def update_base_task(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser),
                     obj_in: BaseTaskUpdate) -> BaseTask:
    base_task = crud_base_task.get(db, id=obj_in.base_task_id)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=base_task.course_id)

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


@router.delete('/{short_name}', response_model=BaseTask)
def delete_base_task(*, db: Session = Depends(get_db), short_name: str,
                     current_user: User = Depends(get_current_active_user)) -> Any:
    base_task = crud_base_task.get_by_short_name(db, short_name=short_name)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=base_task.course_id)

    crud_task.remove_all_to_task_id(db, base_task_id=base_task.id)
    crud_user_solution.remove_all_to_base_task(db, base_task_id=base_task.id)
    crud_base_task.remove(db, model_id=base_task.id)
    return base_task


@router.get('/noGroup', response_model=List[BaseTask])
def get_base_tasks_with_no_group(*, db: Session = Depends(get_db), course_id: int,
                                 current_user: User = Depends(get_current_active_user)) -> Any:
    base_tasks = crud_base_task.get_multi_with_no_task_group(db, course_id=course_id)
    return base_tasks


@router.post('/task', response_model=Task)
def create_task(*, db: Session = Depends(get_db), task_create: TaskCreate,
                current_user: User = Depends(get_current_active_superuser)) -> Any:
    print(task_create)
    check_if_user_can_access_task(db, user_id=current_user.id, base_task_id=task_create.base_task_id)

    task = crud_task.create(db, obj_in=task_create)

    base_task = crud_base_task.get(db, task.base_task_id)
    course = crud_course.get(db=db, id=base_task.course_id)

    for member in course.members:
        if not crud_task.has_new_task(db=db, user_id=member.id, base_task_id=base_task.id):
            crud_task.create_new_task(db=db, base_task_id=base_task.id, user_id=member.id)

    return task


@router.post('/task/{task_id}/annotationGroup', response_model=AnnotationGroup)
def create_annotation_group(*, db: Session = Depends(get_db), task_id: int,
                            annotation_group_create: AnnotationGroup,
                            current_user: User = Depends(get_current_active_superuser)) -> Any:
    task = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(db, user_id=current_user.id, base_task_id=task.base_task_id)

    new_group = {"name": annotation_group_create.name, "color": annotation_group_create.color}
    annotation_groups = task.annotation_groups + [new_group] if task.annotation_groups else [new_group]
    crud_task.update(db, db_obj=task, obj_in=TaskUpdate(annotation_groups=annotation_groups))
    return new_group


@router.put('/task/{task_id}/annotationGroup', response_model=AnnotationGroup)
def update_annotation_group(*, db: Session = Depends(get_db), task_id: int,
                            annotation_group_update: AnnotationGroupUpdate,
                            current_user: User = Depends(get_current_active_superuser)) -> Any:
    task = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(db, user_id=current_user.id, base_task_id=task.base_task_id)

    annotation_group = None
    index = None
    for idx, group in enumerate(task.annotation_groups):
        if group["name"] == annotation_group_update.oldName:
            annotation_group = group
            index = idx
    if annotation_group is not None and index is not None:
        annotation_group["name"] = annotation_group_update.name
        annotation_group["color"] = annotation_group_update.color
        task.annotation_groups[index] = annotation_group
    groups = task.annotation_groups
    task = crud_task.update(db, db_obj=task, obj_in=TaskUpdate(annotation_groups=[]))
    task = crud_task.update(db, db_obj=task, obj_in=TaskUpdate(annotation_groups=groups))
    return annotation_group


@router.delete('/task/{task_id}', response_model=Task)
def delete_task(*, db: Session = Depends(get_db), task_id: int,
                current_user: User = Depends(get_current_active_superuser)) -> Any:
    task_to_delete = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(db, user_id=current_user.id, base_task_id=task_to_delete.base_task_id)

    task = crud_task.remove(db, model_id=task_id)

    crud_user_solution.remove_all_by_task_id(db, task_id=task_id)

    return task


@router.delete('/task/{task_id}/annotations', response_model=Task)
def delete_task_annotations(*, db: Session = Depends(get_db), task_id: int,
                            current_user: User = Depends(get_current_active_superuser)) -> Any:
    task = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(db, user_id=current_user.id, base_task_id=task.base_task_id)

    update = TaskUpdate()
    if task.task_data is not None:
        update.task_data = None
    if task.solution is not None:
        update.solution = None
    return crud_task.update(db, db_obj=task, obj_in=update)


@router.post('/task/{task_id}/annotations', response_model=Any)
def add_task_annotation(*, db: Session = Depends(get_db), task_id: int,
                        annotation: Union[OffsetPolygonData, OffsetLineData, OffsetPointData, AnnotationData],
                        current_user: User = Depends(get_current_active_superuser)) -> Any:
    task = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(db, user_id=current_user.id, base_task_id=task.base_task_id)

    if annotation.type == AnnotationType.BASE:
        if task.task_data is None:
            data = [annotation]
        else:
            data = task.task_data
            data.append(annotation)
        crud_task.update(db, db_obj=task, obj_in=TaskUpdate(task_data=data))
    else:
        if task.solution is None:
            solution = [annotation]
        else:
            solution = task.solution
            solution.append(annotation)
        crud_task.update(db, db_obj=task, obj_in=TaskUpdate(solution=solution))
    return {"Status": "OK"}


@router.put('/task/{task_id}/{annotation_id}', response_model=Any)
def update_task_annotation(*, db: Session = Depends(get_db), task_id: int, annotation_id: str,
                           annotation: Union[OffsetPolygonData, OffsetLineData, OffsetPointData, AnnotationData],
                           current_user: User = Depends(get_current_active_superuser)) -> Any:
    task = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(db, user_id=current_user.id, base_task_id=task.base_task_id)

    if annotation.type == AnnotationType.BASE:
        old_annotation_index = next((index for (index, d) in enumerate(task.task_data) if d["id"] == annotation_id),
                                    None)
        task.task_data[old_annotation_index] = annotation
        task_data = task.task_data
        crud_task.update(db, db_obj=task, obj_in=TaskUpdate(task_data=task_data))
    else:
        old_annotation_index = next((index for (index, d) in enumerate(task.solution) if d["id"] == annotation_id),
                                    None)
        task.solution[old_annotation_index] = annotation
        solution = task.solution
        crud_task.update(db, db_obj=task, obj_in=TaskUpdate(solution=solution))
    return {"Status": "Ok"}


@router.delete('/task/{task_id}/{annotation_id}', response_model=Any)
def delete_task_annotation(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser),
                           task_id: int, annotation_id: str) -> Any:
    task = crud_task.get(db, id=task_id)
    check_if_user_can_access_task(db, user_id=current_user.id, base_task_id=task.base_task_id)

    solution = task.solution

    if solution:
        solution = [d for d in solution if d.get("id") != annotation_id]

    task_data = task.task_data
    if task_data:
        task_data = [d for d in task_data if d.get("id") != annotation_id]

    crud_task.update(db, db_obj=task, obj_in=TaskUpdate(solution=solution, task_data=task_data))
    return {"Status": "OK"}


@router.put('/task', response_model=Task)
def update_task(*, db: Session = Depends(get_db), task_in: TaskUpdate,
                current_user: User = Depends(get_current_active_superuser)) -> Any:
    if task_in.solution:
        task_in.solution = json.loads(task_in.solution)
    if task_in.task_data:
        task_in.task_data = json.loads(task_in.task_data)

    task = crud_task.get(db, id=task_in.task_id)
    base_task = crud_base_task.get(db, id=task.base_task_id)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=base_task.course_id)

    task = crud_task.update(db, db_obj=task, obj_in=task_in)
    return task


@router.delete('/task/{task_id}/userSolution/taskResult', response_model=Any)
def delete_task_result(*, db: Session = Depends(get_db), task_id: int,
                       current_user: User = Depends(get_current_active_user)) -> Any:
    user_solution = crud_user_solution.get_solution_to_task_and_user(db=db, task_id=task_id, user_id=current_user.id)
    temp = crud_user_solution.update(db=db, db_obj=user_solution,
                                     obj_in=UserSolutionUpdate(task_result=None, percentage_solved=0.00))
    return temp


@router.post('/userSolution', response_model=UserSolution)
def save_user_solution(*, db: Session = Depends(get_db), user_solution_in: UserSolutionCreate,
                       current_user: User = Depends(get_current_active_user)) -> Any:
    user_solution = crud_user_solution.get_solution_to_task_and_user(db, user_id=current_user.id,
                                                                     task_id=user_solution_in.task_id)
    if user_solution is not None:
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
    if len(user_solution_in.solution_data) == 0:
        item = crud_user_solution.remove_by_user_id_and_task_id(db, user_id=current_user.id,
                                                                task_id=task_id)
        item.solution_data = user_solution_in.solution_data
        return item

    db_obj = crud_user_solution.get_solution_to_task_and_user(db, task_id=task_id,
                                                              user_id=current_user.id)
    solution = crud_user_solution.update(db, db_obj=db_obj, obj_in=user_solution_in)
    return solution


@router.post('/task/{task_id}/userSolution', response_model=Any)
def add_user_solution_annotation(*, db: Session = Depends(get_db), task_id: int,
                                 current_user: User = Depends(get_current_active_user),
                                 annotation_data: AnnotationData) -> Any:
    user_solution = crud_user_solution.get_solution_to_task_and_user(db, task_id=task_id, user_id=current_user.id)
    data = user_solution.solution_data
    data.append(annotation_data)

    crud_user_solution.update(db, db_obj=user_solution, obj_in=UserSolutionUpdate(solution_data=data))
    return {"status": "OK"}


@router.delete('/task/{task_id}/userSolution/{annotation_id}', response_model=Any)
def delete_user_solution_annotation(*, db: Session = Depends(get_db), task_id: int, annotation_id: str,
                                    current_user: User = Depends(get_current_active_user)) -> Any:
    user_solution = crud_user_solution.get_solution_to_task_and_user(db, task_id=task_id, user_id=current_user.id)
    solution_data = user_solution.solution_data
    if user_solution.solution_data:
        solution_data = [d for d in solution_data if d.get("id") != annotation_id]

    if len(solution_data) == 0:
        delete_item = crud_user_solution.remove_by_user_id_and_task_id(db, user_id=current_user.id, task_id=task_id)
        delete_item.solution_data = solution_data
        return {"Status": "OK"}
    crud_user_solution.update(db, db_obj=user_solution, obj_in=UserSolutionUpdate(solution_data=solution_data))
    return {"Status": "OK"}


@router.put('/task/{task_id}/userSolution/{annotation_id}', response_model=Any)
def update_user_solution_annotation(*, db: Session = Depends(get_db), task_id: int, annotation_id: str,
                                    annotation: AnnotationData,
                                    current_user: User = Depends(get_current_active_user)) -> Any:
    timer = Timer()
    timer.start()

    user_solution = crud_user_solution.get_solution_to_task_and_user(db=db, user_id=current_user.id, task_id=task_id)
    ColoredPrinter.print_lined_info(f"{timer.time_elapsed}")

    old_annotation_index = next(
        (index for (index, d) in enumerate(user_solution.solution_data) if d["id"] == annotation_id), None)

    ColoredPrinter.print_lined_info(f"{timer.time_elapsed}")

    user_solution.solution_data[old_annotation_index] = annotation
    crud_user_solution.update(db, db_obj=user_solution,
                              obj_in=UserSolutionUpdate(solution_data=user_solution.solution_data))
    ColoredPrinter.print_lined_info(f"{timer.time_elapsed}")
    timer.stop()

    return {"Status", "Ok"}


@router.get('/{task_id}/solve', response_model=TaskFeedback)
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
        solution_update.percentage_solved = 0.0

    crud_user_solution.update(db, db_obj=user_solution, obj_in=solution_update)
    timer.stop()
    ColoredPrinter.print_lined_info(f"Completet in {timer.total_run_time * 1000}ms")
    return task_result


@router.get('/task/{task_id}/solution', response_model=List[Union[OffsetPolygonData, OffsetLineData, OffsetPointData]])
def get_task_solution(*, db: Session = Depends(get_db), task_id: int,
                      current_user: User = Depends(get_current_active_user)) -> Any:
    user_solution = crud_user_solution.get_solution_to_task_and_user(db, task_id=task_id, user_id=current_user.id)
    if user_solution is not None and user_solution.percentage_solved == 1:
        task = crud_task.get(db=db, id=task_id)
        return task.solution
    return None


@router.post('/task/{task_id}/hint', response_model=TaskHint)
def create_task_hint(*, db: Session = Depends(get_db), task_id: int,
                     current_user: User = Depends(get_current_active_superuser), task_hint_in: TaskHintCreate) -> Any:
    print("here")
    task = crud_task.get(db, id=task_id)
    base_task = crud_base_task.get(db, id=task.base_task_id)
    check_if_user_can_access_course(db, user_id=current_user.id, course_id=base_task.course_id)
    obj = crud_task_hint.create(db, obj_in=task_hint_in)
    return obj

@router.put('/task/{task_id}/hint/{hint_id}', response_model=TaskHint)
def update_task_hint(*, db: Session = Depends(get_db), task_id: int, hint_id: int,
                     current_user: User = Depends(get_current_active_superuser), task_hint_in: TaskHintUpdate) -> Any:
    task = crud_task.get(db, id=task_id)
    base_task = crud_base_task.get(db, id=task.base_task_id)
    check_if_user_can_access_course(db, user_id=current_user.id, course_id=base_task.course_id)

    print(hint_id)
    hint = crud_task_hint.get(db, id=hint_id)

    obj = crud_task_hint.update(db, db_obj=hint, obj_in=task_hint_in)
    return obj

@router.post('/hint/{hint_id}/image', response_model=Dict)
def upload_task_hint_image(*, db: Session = Depends(get_db), hint_id: int, current_user: User = Depends(get_current_active_superuser), image: UploadFile = File(...)) -> Any:
    
    image_name = uuid.uuid4()

    file_name = f"{image_name}.{image.filename.split('.')[-1]}"

    try:
        minio_client.create_object(file_name, image.file.fileno(), image.content_type)
        return { "path": minio_client.bucket_name + '/' + file_name }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Image could not be saved"
        )
    
