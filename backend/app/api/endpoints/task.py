import json
import os
import uuid
from typing import Any, Dict, List, Union

import pyvips
from app.api.deps import (
    check_if_user_can_access_course,
    check_if_user_can_access_task,
    get_current_active_superuser,
    get_current_active_user,
    get_db,
)
from app.core.export.task_exporter import TaskExporter
from app.crud.crud_base_task import crud_base_task
from app.crud.crud_course import crud_course
from app.crud.crud_hint_image import crud_hint_image
from app.crud.crud_task import crud_task
from app.crud.crud_task_hint import crud_task_hint
from app.crud.crud_task_statistic import crud_task_statistic
from app.crud.crud_user_solution import crud_user_solution
from app.models.user import User
from app.schemas.hint_image import HintImageCreate
from app.schemas.polygon_data import (
    AnnotationData,
    AnnotationType,
    InfoAnnotationData,
    OffsetLineData,
    OffsetPointData,
    OffsetPolygonData,
    OffsetRectangleData,
    RectangleData,
)
from app.schemas.task import (
    AnnotationGroup,
    AnnotationGroupUpdate,
    Task,
    TaskCreate,
    TaskType,
    TaskUpdate,
)
from app.schemas.task_hint import TaskHint, TaskHintCreate, TaskHintUpdate
from app.schemas.user_solution import UserSolutionUpdate
from app.core.annotation_type import is_info_annotation
from app.utils.minio_client import MinioClient, minio_client
from app.utils.timer import Timer
from fastapi import APIRouter, Depends, HTTPException
from fastapi.datastructures import UploadFile
from fastapi.params import File
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

router = APIRouter()


@router.post("", response_model=Task)
def create_task(
    *,
    db: Session = Depends(get_db),
    task_create: TaskCreate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    check_if_user_can_access_task(
        db, user_id=current_user.id, base_task_id=task_create.base_task_id
    )

    task = crud_task.create(db, obj_in=task_create)

    base_task = crud_base_task.get(db, task.base_task_id)
    course = crud_course.get(db=db, id=base_task.course_id)

    for member in course.members:
        if not crud_task.has_new_task(
            db=db, user_id=member.id, base_task_id=base_task.id
        ):
            crud_task.create_new_task(
                db=db, base_task_id=base_task.id, user_id=member.id
            )

    return task


@router.put("", response_model=Task)
def update_task(
    *,
    db: Session = Depends(get_db),
    task_in: TaskUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    if task_in.solution:
        task_in.solution = json.loads(task_in.solution)
    if task_in.task_data:
        task_in.task_data = json.loads(task_in.task_data)

    task = crud_task.get(db, id=task_in.task_id)
    base_task = crud_base_task.get(db, id=task.base_task_id)

    check_if_user_can_access_course(
        db, user_id=current_user.id, course_id=base_task.course_id
    )

    task = crud_task.update(db, db_obj=task, obj_in=task_in)
    return task


@router.post("/{task_id}/annotationGroup", response_model=AnnotationGroup)
def create_annotation_group(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    annotation_group_create: AnnotationGroup,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    task = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(
        db, user_id=current_user.id, base_task_id=task.base_task_id
    )

    new_group = {
        "name": annotation_group_create.name,
        "color": annotation_group_create.color,
    }
    annotation_groups = (
        task.annotation_groups + [new_group] if task.annotation_groups else [new_group]
    )
    crud_task.update(
        db, db_obj=task, obj_in=TaskUpdate(annotation_groups=annotation_groups)
    )
    return new_group


@router.put("/{task_id}/annotationGroup", response_model=AnnotationGroup)
def update_annotation_group(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    annotation_group_update: AnnotationGroupUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    task = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(
        db, user_id=current_user.id, base_task_id=task.base_task_id
    )

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

    user_solutions = crud_user_solution.get_solution_to_task(db, task_id=task.id)

    for user_solution in user_solutions:
        for annotation in user_solution.solution_data:
            if (
                "name" in annotation
                and annotation["name"] == annotation_group_update.oldName
            ):
                annotation["name"] = annotation_group_update.name
                annotation["color"] = annotation_group_update.color
        crud_user_solution.update(
            db,
            obj_in=UserSolutionUpdate(solution_data=user_solution.solution_data),
            db_obj=user_solution,
        )

    if task.solution is not None:
        for annotation in task.solution:
            if (
                "name" in annotation
                and annotation["name"] == annotation_group_update.oldName
            ):
                annotation["name"] = annotation_group_update.name
                annotation["color"] = annotation_group_update.color
    crud_task.update(
        db,
        db_obj=task,
        obj_in=TaskUpdate(annotation_groups=groups, solution=task.solution),
    )
    return annotation_group


@router.delete("/{task_id}", response_model=Task)
def delete_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    try:
        task_to_delete = crud_task.get(db, id=task_id)

        check_if_user_can_access_task(
            db, user_id=current_user.id, base_task_id=task_to_delete.base_task_id
        )

        crud_user_solution.remove_all_by_task_id(db, task_id=task_id)

        crud_task_statistic.remove_all_by_task_id(db, task_id=task_id)

        if task_to_delete.task_type == TaskType.IMAGE_SELECT:
            for image in task_to_delete.task_data:
                minio_client.bucket_name = MinioClient.task_bucket
                minio_client.delete_object(image)

        task = crud_task.remove(db, model_id=task_id)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Task could not be deleted")

    return task


@router.delete("/{task_id}/annotations", response_model=Task)
def delete_task_annotations(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    task = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(
        db, user_id=current_user.id, base_task_id=task.base_task_id
    )

    update = TaskUpdate()
    if task.task_data is not None:
        update.task_data = None
    if task.solution is not None:
        update.solution = None

    if task.info_annotations is not None:
        task.info_annotations = None

    return crud_task.update(db, db_obj=task, obj_in=update)


@router.post("/{task_id}/annotations", response_model=Any)
def add_task_annotation(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    annotation: Union[
        OffsetRectangleData,
        OffsetPolygonData,
        OffsetLineData,
        OffsetPointData,
        RectangleData,
        InfoAnnotationData,
        AnnotationData,
    ],
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    task = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(
        db, user_id=current_user.id, base_task_id=task.base_task_id
    )

    # annotation_is_valid = check_if_annotation_is_valid(annotation)

    # if annotation_is_valid is not None and not annotation_is_valid:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Annotation is invalid"
    #     )
    if annotation.type == AnnotationType.BASE:
        if task.task_data is None:
            data = [annotation]
        else:
            data = task.task_data
            data.append(annotation)
        crud_task.update(db, db_obj=task, obj_in=TaskUpdate(task_data=data))

    elif is_info_annotation(annotation.type):

        if task.info_annotations is None:
            data = [annotation]
        else:
            data = task.info_annotations
            data.append(annotation)
        crud_task.update(db, db_obj=task, obj_in=TaskUpdate(info_annotations=data))

    else:
        if task.solution is None:
            solution = [annotation]
        else:
            solution = task.solution
            solution.append(annotation)
        crud_task.update(db, db_obj=task, obj_in=TaskUpdate(solution=solution))
    return {"Status": "OK"}


@router.put("/{task_id}/{annotation_id}", response_model=Any)
def update_task_annotation(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    annotation_id: str,
    annotation: Union[
        OffsetRectangleData,
        OffsetPolygonData,
        OffsetLineData,
        OffsetPointData,
        RectangleData,
        InfoAnnotationData,
        AnnotationData,
    ],
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    task = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(
        db, user_id=current_user.id, base_task_id=task.base_task_id
    )

    if annotation.type == AnnotationType.BASE:
        old_annotation_index = next(
            (
                index
                for (index, d) in enumerate(task.task_data)
                if d["id"] == annotation_id
            ),
            None,
        )
        task.task_data[old_annotation_index] = annotation
        task_data = task.task_data
        crud_task.update(db, db_obj=task, obj_in=TaskUpdate(task_data=task_data))
    elif is_info_annotation(annotation.type):
        old_annotation_index = next(
            (
                index
                for (index, d) in enumerate(task.info_annotations)
                if d["id"] == annotation_id
            ),
            None,
        )
        task.info_annotations[old_annotation_index] = annotation
        info_annotations = task.info_annotations
        crud_task.update(
            db, db_obj=task, obj_in=TaskUpdate(info_annotations=info_annotations)
        )
    else:
        old_annotation_index = next(
            (
                index
                for (index, d) in enumerate(task.solution)
                if d["id"] == annotation_id
            ),
            None,
        )
        task.solution[old_annotation_index] = annotation
        solution = task.solution
        crud_task.update(db, db_obj=task, obj_in=TaskUpdate(solution=solution))
    return {"Status": "Ok"}


@router.delete("/{task_id}/{annotation_id}", response_model=Any)
def delete_task_annotation(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
    task_id: int,
    annotation_id: str,
) -> Any:
    task = crud_task.get(db, id=task_id)
    check_if_user_can_access_task(
        db, user_id=current_user.id, base_task_id=task.base_task_id
    )

    solution = task.solution

    if solution:
        solution = [d for d in solution if d.get("id") != annotation_id]

    task_data = task.task_data
    if task_data:
        task_data = [d for d in task_data if d.get("id") != annotation_id]

    info_annotations = task.info_annotations
    if info_annotations:
        info_annotations = [d for d in info_annotations if d.get("id") != annotation_id]

    crud_task.update(
        db,
        db_obj=task,
        obj_in=TaskUpdate(
            solution=solution, task_data=task_data, info_annotations=info_annotations
        ),
    )
    return {"Status": "OK"}


@router.delete("/{task_id}/userSolution/taskResult", response_model=Any)
def delete_task_result(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    user_solution = crud_user_solution.get_solution_to_task_and_user(
        db=db, task_id=task_id, user_id=current_user.id
    )
    temp = crud_user_solution.update(
        db=db,
        db_obj=user_solution,
        obj_in=UserSolutionUpdate(task_result=None, percentage_solved=0.00),
    )
    return temp


@router.get(
    "/{task_id}/userSolution/download", response_model=Any, response_description="xlsx"
)
def download_usersolutions(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    task = crud_task.get(db, id=task_id)

    check_if_user_can_access_task(
        db, user_id=current_user.id, base_task_id=task.base_task_id
    )

    output = TaskExporter.export_point_task_as_xlsx(db, task)

    headers = {"Content-Disposition": 'attachment; filename="' + str(task.id) + '"'}

    return StreamingResponse(output, headers=headers)


@router.post("/{task_id}/userSolution", response_model=Any)
def add_user_solution_annotation(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    annotation_data: Union[RectangleData, AnnotationData],
) -> Any:
    user_solution = crud_user_solution.get_solution_to_task_and_user(
        db, task_id=task_id, user_id=current_user.id
    )
    data = user_solution.solution_data
    data.append(annotation_data)

    crud_user_solution.update(
        db, db_obj=user_solution, obj_in=UserSolutionUpdate(solution_data=data)
    )
    return {"status": "OK"}


@router.put("/{task_id}/userSolution/{annotation_id}", response_model=Any)
def update_user_solution_annotation(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    annotation_id: str,
    annotation: Union[RectangleData, AnnotationData],
    current_user: User = Depends(get_current_active_user),
) -> Any:
    timer = Timer()
    timer.start()

    user_solution = crud_user_solution.get_solution_to_task_and_user(
        db=db, user_id=current_user.id, task_id=task_id
    )

    old_annotation_index = next(
        (
            index
            for (index, d) in enumerate(user_solution.solution_data)
            if d["id"] == annotation_id
        ),
        None,
    )

    user_solution.solution_data[old_annotation_index] = annotation
    crud_user_solution.update(
        db,
        db_obj=user_solution,
        obj_in=UserSolutionUpdate(solution_data=user_solution.solution_data),
    )
    timer.stop()

    return {"Status", "Ok"}


@router.delete("/{task_id}/userSolution/{annotation_id}", response_model=Any)
def delete_user_solution_annotation(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    annotation_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    user_solution = crud_user_solution.get_solution_to_task_and_user(
        db, task_id=task_id, user_id=current_user.id
    )
    solution_data = user_solution.solution_data
    if user_solution.solution_data:
        solution_data = [d for d in solution_data if d.get("id") != annotation_id]

    # if len(solution_data) == 0:
    #     delete_item = crud_user_solution.remove_by_user_id_and_task_id(db, user_id=current_user.id, task_id=task_id)
    #     delete_item.solution_data = solution_data
    #     return {"Status": "OK"}
    crud_user_solution.update(
        db, db_obj=user_solution, obj_in=UserSolutionUpdate(solution_data=solution_data)
    )
    return {"Status": "OK"}


@router.get(
    "/{task_id}/solution",
    response_model=List[Union[OffsetPolygonData, OffsetLineData, OffsetPointData]],
)
def get_task_solution(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    user_solution = crud_user_solution.get_solution_to_task_and_user(
        db, task_id=task_id, user_id=current_user.id
    )
    if user_solution is not None and user_solution.percentage_solved == 1:
        task = crud_task.get(db=db, id=task_id)
        return task.solution
    return None


@router.post("/{task_id}/hint", response_model=TaskHint)
def create_task_hint(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_active_superuser),
    task_hint_in: TaskHintCreate,
) -> Any:
    task = crud_task.get(db, id=task_id)
    base_task = crud_base_task.get(db, id=task.base_task_id)
    check_if_user_can_access_course(
        db, user_id=current_user.id, course_id=base_task.course_id
    )

    task_hint_create = task_hint_in.copy(deep=True)

    task_hint_create.images = []
    obj = crud_task_hint.create(db, obj_in=task_hint_create)

    hint_id = obj.id
    for image in task_hint_in.images:
        crud_hint_image.create(
            db,
            obj_in=HintImageCreate(task_hint_id=hint_id, image_name=image.image_name),
        )

    db.refresh(obj)

    return obj


@router.put("/{task_id}/hint/{hint_id}", response_model=TaskHint)
def update_task_hint(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    hint_id: int,
    current_user: User = Depends(get_current_active_superuser),
    task_hint_in: TaskHintUpdate,
) -> Any:
    task = crud_task.get(db, id=task_id)
    base_task = crud_base_task.get(db, id=task.base_task_id)
    check_if_user_can_access_course(
        db, user_id=current_user.id, course_id=base_task.course_id
    )

    hint = crud_task_hint.get(db, id=hint_id)

    obj = crud_task_hint.update(db, db_obj=hint, obj_in=task_hint_in)

    if len(task_hint_in.images) == 0:
        for image in obj.images:
            crud_hint_image.remove(db, model_id=image.id)
    else:
        task_hint_image_names = [image.image_name for image in obj.images]
        in_image_names = [image.image_name for image in task_hint_in.images]
        deleted_images_names = set(task_hint_image_names).difference(in_image_names)
        new_images_names = (
            set(in_image_names)
            .difference(task_hint_image_names)
            .difference(deleted_images_names)
        )

        for new_image_name in new_images_names:
            obj.images.append(
                crud_hint_image.create(
                    db,
                    obj_in=HintImageCreate(
                        task_hint_id=hint_id, image_name=new_image_name
                    ),
                )
            )

        result_images = []

        for image in obj.images:
            if image.image_name in deleted_images_names:
                crud_hint_image.remove(db, model_id=image.id)
            else:
                result_images.append(image)

        obj.images = result_images
    db.refresh(obj)
    return obj


@router.post("/images", response_model=List[Dict])
def upload_task_image(
    *,
    current_user: User = Depends(get_current_active_superuser),
    images: List[UploadFile] = File(...),
):
    results = []

    for image in images:
        image_name = uuid.uuid4()

        file_name = f"{image_name}.{image.filename.split('.')[-1]}"

        final_name = f"{image_name}.jpeg"

        pyvips_image = pyvips.Image.new_from_buffer(image.file.read(), options="")

        pyvips_image.jpegsave(final_name, Q=75)

        try:
            minio_client.bucket_name = MinioClient.task_bucket
            minio_client.create_object(file_name, final_name, "image/jpeg")
            os.remove(final_name)
            results.append(
                {
                    "path": minio_client.bucket_name + "/" + file_name,
                    "old_name": image.filename,
                }
            )
        except Exception as e:
            print(e)
            os.remove(final_name)
            raise HTTPException(status_code=500, detail="Image could not be saved")
    return results


# @router.post('/image', response_model=Dict)
# def upload_task_image(*, current_user: User = Depends(get_current_active_superuser), image: UploadFile = File(...)):
#     image_name = uuid.uuid4()
#
#     file_name = f"{image_name}.{image.filename.split('.')[-1]}"
#
#     final_name = f'{image_name}.jpeg'
#
#     pyvips_image = pyvips.Image.new_from_buffer(image.file.read(), options="")
#
#     pyvips_image.jpegsave(final_name, Q=75)
#
#     try:
#         minio_client.bucket_name = MinioClient.task_bucket
#         minio_client.create_object(final_name, final_name, "image/jpeg")
#         os.remove(final_name)
#         return {"path": minio_client.bucket_name + '/' + final_name, "old_name": image.filename}
#     except Exception as e:
#         print(e)
#         os.remove(final_name)
#         raise HTTPException(
#             status_code=500,
#             detail="Image could not be saved"
#         )
#
#
# @router.delete('/image/minio/{image_path}', response_model=Dict)
# def delete_task_image(*, current_user: User = Depends(get_current_active_superuser), image_path: str):
#     try:
#         minio_client.bucket_name = MinioClient.task_bucket
#         minio_client.delete_object('/task-images/' + image_path)
#         return {"Status": "Ok"}
#     except Exception as e:
#         print(e)
#         raise HTTPException(
#             status_code=500,
#             detail="Image could not be deleted"
#         )
