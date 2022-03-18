import uuid
from typing import Dict, List

from app import app
from app.crud.crud_slide import crud_slide
from app.db.deps import get_slide_collection
from app.schemas.slide import CreateSlide, Slide, SlideStatus
from app.utils.file_utils import write_slide_to_disk
from app.utils.slide_utils import (convert_binary_metadata_to_base64,
                                   convert_slide_binary_metadata_to_base64)
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.params import Depends, File, Form, Query
from pymongo.collection import Collection
from starlette.background import BackgroundTasks

router = APIRouter()


@router.post('')
def create_slide(*, collection: Collection = Depends(get_slide_collection), background_tasks: BackgroundTasks,
                 name: str = Form(...), file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_type = file.filename.split('.')[-1]
    file_name = f"{file_id}.{file_type}"

    if crud_slide.slide_with_name_exists(collection=collection, name=name):
        raise HTTPException(
            status_code=400,
            detail="Slide with this name already exists"
        )

    try:
        crud_slide.create(collection, obj_in=CreateSlide(
            slide_id=file_id,
            name=name,
            status=SlideStatus.RUNNING
        ))

        background_tasks.add_task(
            write_slide_to_disk, file_id, file_name, file=file)
    except Exception as e:
        print(e)
        crud_slide.delete(collection, entity_id_value=file_id)
        raise HTTPException(
            status_code=500,
            detail="Slide couldn't be saved"
        )

    return Slide(
        slide_id=file_id,
        name=name,
        status=SlideStatus.RUNNING
    )


@router.get('', response_model=List[Slide])
def read_slides(*, collection: Collection = Depends(get_slide_collection), slideid: List[str] = Query(None),
                status: SlideStatus = Query(None),
                metadata: bool = Query(True)) -> List[Slide]:
    if slideid:
        slides = crud_slide.get_all_slides_by_ids(
            collection=collection,
            slide_ids=slideid,
            status=status,
            with_metadata=metadata
        )
    else:
        slides = crud_slide.get_all_slides(
            collection=collection,
            status=status,
            with_metadata=metadata
        )
    if metadata:
        slides = convert_binary_metadata_to_base64(slides)
    return slides


@router.get('/{slide_id}')
def get_slide_by_id(*, collection: Collection = Depends(get_slide_collection), slide_id: str, metadata: bool = Query(True)):
    slide = crud_slide.get_slide(collection=collection, slide_id=slide_id, with_metadata=metadata)
    if metadata:
        slide = convert_slide_binary_metadata_to_base64(slide)
    return slide


@router.get('/{slide_id}/name')
def get_slide(*, collection: Collection = Depends(get_slide_collection), slide_id: str):
    slide = crud_slide.get_slide(collection=collection, slide_id=slide_id, with_metadata=False)
    return {"name": slide.name}


@router.delete('/{slide_id}')
def delete_slide(*, collection: Collection = Depends(get_slide_collection), slide_id: str):
    try:
        app.minio_wrapper.delete_slide(slide_id)
        crud_slide.delete(collection, entity_id_value=slide_id)
        # slide_db.delete_slide(slide_id=slide_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Slide could not be deleted"
        )
