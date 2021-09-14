import os
import shutil
import uuid
from typing import Any

import aiofiles
from fastapi import UploadFile, Form, File, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from app.api.deps import get_db, get_current_active_superuser, get_current_active_user
from app.core.polygon_extractor import convert_image_to_annotations
from app.crud.crud_base_task import crud_base_task
from app.crud.crud_slide import crud_slide
from app.db.session import SessionLocal
from app.models.slide import Slide as SlideModel
from app.models.user import User as SchemaUser
from app.worker.tasks import celery_app

router = APIRouter()


async def write_slide(name: str, file: UploadFile):
    db = SessionLocal()
    file_id = uuid.uuid4()
    file_extension = os.path.splitext(file.filename)[1]
    file_name = str(file_id) + file_extension

    # Save Slide in Database
    slide = SlideModel()
    slide.file_id = str(file_id)
    slide.status = 'R'
    slide.name = str(name)
    crud_slide.create(db=db, slide=slide)

    async with aiofiles.open(f"./data/{file_name}", 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    # Start Celery Task
    task = celery_app.send_task("create_slide.task", args=[file_name])
    return {"Result": "OK"}


@router.post('/convert')
async def convert_image(*, file: UploadFile = File(...),
                        current_user: SchemaUser = Depends(get_current_active_user)) -> Any:
    contents = await file.read()
    result = convert_image_to_annotations(contents)
    return result


@router.post('')
async def upload(background_task: BackgroundTasks, name: str = Form(...), file: UploadFile = File(...),
                 db: Session = Depends(get_db), current_user: SchemaUser = Depends(get_current_active_superuser)):
    duplicate_slide = crud_slide.get_by_name(db, name=name)
    if duplicate_slide:
        raise HTTPException(
            status_code=400,
            detail="Name already exists"
        )

    try:
        file_id = uuid.uuid4()
        file_extension = os.path.splitext(file.filename)[1]
        file_name = str(file_id) + file_extension

        async with aiofiles.open(f"./data/{file_name}", 'wb') as out_file:
            while content := await file.read(1024):  # async read chunk
                await out_file.write(content)  # async write chunk

        # Save Slide in Database
        slide = SlideModel()
        slide.file_id = str(file_id)
        slide.status = 'R'
        slide.name = str(name)
        crud_slide.create(db=db, obj_in=slide)

        # Start Celery Task
        celery_app.send_task("create_slide.task", args=[file_name])
        return {"Result": "OK"}

    except Exception as exc:
        print(exc)
        db.rollback()
        return {"Result": "Error"}


@router.get("")
def read_slides(db: Session = Depends(get_db), current_user: SchemaUser = Depends(get_current_active_superuser)):
    slides = crud_slide.get_all(db)
    return slides


@router.delete("/{file_id}")
def delete_slide(file_id: str, db: Session = Depends(get_db),
                 current_user: SchemaUser = Depends(get_current_active_superuser)):
    slide = crud_slide.get_by_file_id(db, file_id=file_id)
    slide_is_in_use = crud_base_task.base_task_uses_slide(db, slide_id=slide.id)
    if not slide_is_in_use:
        try:
            crud_slide.remove_by_file_id(db, file_id=file_id)
            os.remove(f"./data/{file_id}.svs")
            shutil.rmtree(f"./data/slide/{file_id}", ignore_errors=True)
        except Exception:
            return {"Result": "Error"}
    else:
        raise HTTPException(
            status_code=409,
            detail="Slide is in use"
        )
    return {"Result": "Ok"}
