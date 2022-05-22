import os
import uuid
from tracemalloc import reset_peak
from typing import List

import pyvips
from app import app
from app.crud.crud_info_image import crud_info_image
from app.db.deps import get_info_image_collection
from app.schemas.info_image import CreateInfoImage, InfoImage, UpdateInfoImage
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from fastapi.params import File, Query
from pymongo.collection import Collection

router = APIRouter()


@router.get("")
def get_info_images_by_id(
    *,
    collection: Collection = Depends(get_info_image_collection),
    infoimageid: List[str] = Query(None),
) -> List[InfoImage]:
    if infoimageid:
        info_images = crud_info_image.get_multi_by_ids(
            collection=collection, ids=infoimageid, filter_query={"_id": False}
        )
    else:
        info_images = crud_info_image.get_multi(
            collection=collection, filter_query={"_id": False}
        )

    return info_images


@router.post("")
def create_info_images(
    *,
    collection: Collection = Depends(get_info_image_collection),
    names: List[str] = Form(...),
    images: List[UploadFile] = File(...),
) -> List[InfoImage]:

    results = []
    for index, image in enumerate(images):
        info_image_id = str(uuid.uuid4())

        info_image_file_name = f"{info_image_id}.jpeg"

        pyvips_image = pyvips.Image.new_from_buffer(image.file.read(), options="")
        pyvips_image.jpegsave(info_image_file_name, Q=75)

        try:
            info_image_object_id = crud_info_image.create(
                collection=collection,
                obj_in=CreateInfoImage(info_image_id=info_image_id, name=names[index]),
            )
            app.minio_wrapper.create_info_image(
                file_name=info_image_file_name, file_content=info_image_file_name
            )
            results.append(
                crud_info_image.get_by_objectId(
                    collection=collection, object_id=info_image_object_id
                )
            )
        except Exception as e:
            print(e)
            os.remove(info_image_file_name)
            app.minio_wrapper.delete_info_image(file_name=info_image_file_name)
            raise HTTPException(status_code=500, detail="Image could not be saved")
    return results


@router.put("")
def update_info_image(
    *,
    collection: Collection = Depends(get_info_image_collection),
    update_schemas: List[UpdateInfoImage],
):
    for update_schema in update_schemas:
        info_image_id = update_schema.info_image_id
        delattr(update_schema, "info_image_id")
        crud_info_image.update(
            collection=collection, obj_in=update_schema, entity_id_value=info_image_id
        )


@router.delete("")
def delete_info_images(
    *, collection: Collection = Depends(get_info_image_collection), images: List[str]
):

    for image_id in images:
        try:
            crud_info_image.delete(collection, entity_id_value=image_id)
            app.minio_wrapper.delete_info_image(file_name=image_id)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Image could not be deleted")
