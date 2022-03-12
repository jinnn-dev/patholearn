import os
import uuid
from typing import List

import pyvips
from app import app
from app.crud.crud_task_image import crud_task_image
from app.db.deps import get_task_image_collection
from app.schemas.task_image import CreateTaskImage, TaskImage, UpdateTaskImage
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from fastapi.params import File, Query
from pymongo.collection import Collection

router = APIRouter()


@router.get('')
def get_task_images_by_id(*, collection: Collection = Depends(get_task_image_collection),
                          taskimageid: List[str] = Query(None)) -> List[TaskImage]:
    if taskimageid:
        task_images = crud_task_image.get_multi_by_ids(collection=collection, ids=taskimageid,
                                                       filter_query={'_id': False})
    else:
        task_images = crud_task_image.get_multi(collection=collection, filter_query={'_id': False})

    return task_images


@router.post('')
def create_task_image(*, collection: Collection = Depends(get_task_image_collection),
                      names: List[str] = Form(...), images: List[UploadFile] = File(...)) -> List[TaskImage]:
    results = []
    for index, image in enumerate(images):
        task_image_id = str(uuid.uuid4())

        task_image_file_name = f"{task_image_id}.jpeg"

        pyvips_image = pyvips.Image.new_from_buffer(image.file.read(), options="")

        pyvips_image.jpegsave(task_image_file_name, Q=75)

        try:
            task_image_object_id = crud_task_image.create(collection=collection, obj_in=CreateTaskImage(
                task_image_id=task_image_id,
                name=names[index]
            ))
            app.minio_wrapper.create_task_image(file_name=task_image_file_name, file_content=task_image_file_name)
            results.append(crud_task_image.get_by_objectId(collection=collection, object_id=task_image_object_id))
        except Exception as e:
            print(e)
            os.remove(task_image_file_name)
            app.minio_wrapper.delete_task_image(file_name=task_image_file_name)
            raise HTTPException(
                status_code=500,
                detail="Image could not be saved"
            )
    return results


@router.put('')
def update_task_image(*, collection: Collection = Depends(get_task_image_collection),
                      update_schemas: List[UpdateTaskImage]):
    for update_schema in update_schemas:
        task_image_id = update_schema.task_image_id
        delattr(update_schema, 'task_image_id')
        crud_task_image.update(collection, obj_in=update_schema, entity_id_value=task_image_id)
