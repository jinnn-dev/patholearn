from typing import Any, List, Union

from app.api.deps import (check_if_user_can_access_course,
                          get_current_active_superuser,
                          get_current_active_user, get_db)
from app.crud.crud_base_task import crud_base_task
from app.crud.crud_course import crud_course
from app.crud.crud_task import crud_task
from app.crud.crud_user_solution import crud_user_solution
from app.models.user import User
from app.schemas.course import Course as CourseSchema
from app.schemas.course import (CourseAdmin, CourseAll, CourseCreate,
                                CourseDetail)
from app.schemas.course import CourseUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

router = APIRouter()


@router.get('', response_model=List[CourseSchema])
def get_all_courses(db: Session = Depends(get_db), search: str = '',
                 current_user: User = Depends(get_current_active_user)) -> Any:
    if search == '':
        return crud_course.get_multi(db)
    return crud_course.get_multi_by_name(db, search=search, user_id=current_user.id)


@router.get('/member', response_model=List[CourseSchema])
def get_courses_of_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)) -> Any:
    courses = crud_course.get_multi_by_user(db, user_id=current_user.id)

    for course in courses:
        course_percentage_solved = crud_user_solution.get_solved_percentage_to_course(
            db, user_id=current_user.id, course_id=course.id
        )
        has_new_task = False
        task_count = 0
        for task_group in course.task_groups:
            ids = [group.id for group in task_group.tasks if group.enabled == True]
            if crud_task.has_new_task_multiple_base_tasks(db=db, user_id=current_user.id, base_task_ids=ids):
                has_new_task = True
            for task in task_group.tasks:
                task_count += len(task.tasks)

        if task_count:
            course.percentage_solved = float(course_percentage_solved) / task_count

        correct_count = crud_user_solution.get_amount_of_correct_solutions_to_course(db=db, user_id=current_user.id,
                                                                                     course_id=course.id)
        wrong_count = crud_user_solution.get_amount_of_wrong_solutions_to_course(db=db, user_id=current_user.id,
                                                                                 course_id=course.id)
        course.correct_tasks = correct_count
        course.wrong_tasks = wrong_count
        course.task_count = task_count
        course.new_tasks = has_new_task
    return courses


@router.get('/owner', response_model=List[CourseSchema])
def get_owned_courses(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)) -> Any:
    """
    Retrieve courses
    :param db:
    :param skip:
    :param limit:
    :param current_user:
    :return:
    """
    courses = crud_course.get_multi_by_owner(db=db, owner_id=current_user.id)

    for course in courses:
        course_percentage_solved = crud_user_solution.get_solved_percentage_to_course(
            db, user_id=current_user.id, course_id=course.id
        )

        task_count = 0
        for task_group in course.task_groups:
            for task in task_group.tasks:
                task_count += len(task.tasks)

        if task_count:
            course.percentage_solved = float(course_percentage_solved) / task_count
        course.task_count = task_count
    return courses


@router.get('/{short_name}', response_model=Union[CourseAdmin, CourseDetail])
def get_specific_course(*, db: Session = Depends(get_db), short_name: str,
                       current_user: User = Depends(get_current_active_user)) -> Any:
    course = crud_course.get_by_short_name(db, short_name=short_name)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    is_member = False
    for member in course.members:
        if member.id == current_user.id:
            is_member = True

    is_owner = course.owner.id == current_user.id

    if not is_member and not is_owner:
        raise HTTPException(
            status_code=403,
            detail={"course": {"name": course.name, "short_name": course.short_name, "owner": {
                "firstname": course.owner.firstname,
                "lastname": course.owner.lastname
            }}}
        )

    course = CourseAll(id=course.id, short_name=course.short_name, name=course.name, created=course.created,
                       members=course.members, is_member=is_member, task_groups=course.task_groups,
                       owner=course.owner, task_count=0)

    course_percentage_solved = 0.0
    task_count = 0
    has_new_tasks = False
    for task_group in course.task_groups:
        percentage = crud_user_solution.get_solved_percentage_to_task_group(
            db, user_id=current_user.id, task_group_id=task_group.id
        )[0] or 0.0

        base_task_count = 0

        ids = [group.id for group in task_group.tasks if group.enabled == True]
        if crud_task.has_new_task_multiple_base_tasks(db, user_id=current_user.id, base_task_ids=ids):
            task_group.new_tasks += 1
            has_new_tasks = True

        for base_task in task_group.tasks:
            if not base_task.enabled and not current_user.is_superuser:
                continue
            base_task_count += len(base_task.tasks)
            task_count += base_task_count
            course_percentage_solved += float(percentage)
            if base_task_count:
                task_group.percentage_solved = percentage / base_task_count
            else:
                task_group.percentage_solved = 0.0
        task_group.task_count = base_task_count
        task_group.correct_tasks = crud_user_solution.get_amount_of_correct_solutions_to_task_group(db,
                                                                                                    user_id=current_user.id,
                                                                                                    task_group_id=task_group.id)
        task_group.wrong_tasks = crud_user_solution.get_amount_of_wrong_solutions_to_task_group(db,
                                                                                                user_id=current_user.id,
                                                                                                task_group_id=task_group.id)

        if task_group.task_count is None:
            task_group.task_count = 0

        delattr(task_group, 'tasks')

    course.percentage_solved = course_percentage_solved
    course.task_count = task_count
    course.new_tasks = int(has_new_tasks)

    if current_user.id != course.owner.id:
        delattr(course, 'members')
    return course


@router.post('/{short_name}', response_model=CourseSchema)
def join_course(*, db: Session = Depends(get_db), short_name: str,
                current_user: User = Depends(get_current_active_user)) -> Any:
    joined_course = crud_course.join_course(db, short_name=short_name, user_id=current_user.id)

    if joined_course is None:
        raise HTTPException(
            status_code=409,
            detail="Already part of the course"
        )
    count = 0
    for task_group in joined_course.task_groups:
        count += len(task_group.tasks)

    joined_course.task_count = count
    return joined_course


@router.delete('/{short_name}/member', response_model=CourseSchema)
def leave_course(*, db: Session = Depends(get_db), short_name: str,
                 current_user: User = Depends(get_current_active_user)) -> Any:
    course = crud_course.get_by_short_name(db, short_name=short_name)
    crud_course.leave_course(db, course_id=course.id, user_id=current_user.id)
    return crud_user_solution.remove_all_by_user_to_course(db, user_id=current_user.id, course_id=course.id)


@router.delete('/{short_name}', response_model=CourseSchema)
def delete_course(*, db: Session = Depends(get_db), short_name: str,
                  current_user: User = Depends(get_current_active_superuser)) -> Any:
        
    course = crud_course.get_by_short_name(db, short_name=short_name)
    check_if_user_can_access_course(db, user_id=current_user.id, course_id=course.id)

    crud_user_solution.remove_all_to_course(db, course_id=course.id)

    for task_group in course.task_groups:
        for base_task in task_group.tasks:
            crud_task.remove_all_to_task_id(db, base_task_id=base_task.id)
            crud_base_task.remove(db, model_id=base_task.id)

    crud_course.remove(db, model_id=course.id)
    return course


@router.post('', response_model=CourseSchema)
def create_course(*, db: Session = Depends(get_db), course_in: CourseCreate,
                  current_user: User = Depends(get_current_active_superuser)) -> Any:
    duplicate_course = crud_course.get_by_name(db, name=course_in.name)
    if duplicate_course:
        raise HTTPException(
            status_code=400,
            detail="The Course with this name already exists"
        )
    course = crud_course.create_with_owner(db=db, obj_in=course_in, owner_id=current_user.id)
    return course


@router.put('', response_model=CourseSchema)
def update_course(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser),
                     obj_in: CourseUpdate) -> CourseSchema:
    course = crud_course.get(db, id=obj_in.course_id)

    check_if_user_can_access_course(db, user_id=current_user.id, course_id=course.id)

    course = crud_course.update(db, db_obj=course, obj_in=obj_in)
    return course