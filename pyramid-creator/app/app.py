import os
import uuid
from typing import List

import aiofiles
from fastapi import BackgroundTasks, FastAPI, HTTPException, UploadFile
from fastapi.params import File, Form
from starlette.middleware.cors import CORSMiddleware

from app.db.database import (CreateSlide, DatabaseSlide, Slide, SlideStatus,
                             slide_db)
from app.persistance.custom_minio_client import MinioClient
from app.utils.util import (convert_binary_metadata_to_base64,
                            convert_binary_to_base64, is_byte_data,
                            write_slide_to_disk)

app = FastAPI()

minio_client = MinioClient()
minio_client.create_bucket("pyramids")

origins = [
    "http://10.168.2.105:3000",
    "http://localhost:3000",
    "http://localhost:8000"
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('')
def test():
    return {"Hello": "World"}


@app.post('/slides')
def create_slide(background_tasks: BackgroundTasks, name: str = Form(...), file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())

    file_name = f"{file_id}.{file.filename.split('.')[1]}"

    if slide_db.slide_with_name_exists(name):
        raise HTTPException(
            status_code=400,
            detail="Slide with this name already exists"
        )

    try:
        slide_db.insert_slide(CreateSlide(
            slide_id=file_id,
            name=name,
            status=SlideStatus.RUNNING
        ))
        background_tasks.add_task(write_slide_to_disk, file_id, file_name, file=file)
    except Exception as e:
        print(e)
        slide_db.delete_slide(slide_id=file_id)
        raise HTTPException(
            status_code=500,
            detail="Slide couldn't be saved"
        )
    return Slide(
                slide_id=file_id,
                name=name,
                status=SlideStatus.RUNNING
            )


@app.get('/slides', response_model=List[Slide])
def read_slides() -> List[Slide]:
    slides = slide_db.get_all_slides()
    slides_without_binary_metadata = convert_binary_metadata_to_base64(slides)
    return slides_without_binary_metadata

@app.get('/slides/{slide_id}/name')
def get_slide(slide_id: str):
    slide = slide_db.get_slide_with_slide_id(slide_id)
    return {"name": slide["name"]}

@app.delete('/slides/{slide_id}')
def delete_slide(slide_id: str):
    try:
        minio_client.delete_slide(slide_id=slide_id)
        slide_db.delete_slide(slide_id=slide_id)
    except Exception as e:
        print(e)


@app.delete('/slides/delete/all')
def delete_all():
    minio_client.delete_all_objects()
    return {"status": "ok"}
