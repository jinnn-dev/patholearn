import os
import uuid

import aiofiles
from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.params import File, Form
from starlette.middleware.cors import CORSMiddleware

# from app.db.database import create_database, create_table, add_slide, all_slides
from app.db.database import slide_db, SlideStatus, CreateSlide
from app.persistance.custom_minio_client import MinioClient
from app.worker import convert_slide

app = FastAPI()

minio_client = MinioClient()
minio_client.create_bucket("pyramids")

origins = [
    "http://10.168.2.105:3000",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def write_file(folder_name: str, file_name: str, file: UploadFile = File(...)):
    async with aiofiles.open(f"/data/{folder_name}/{file_name}", "wb") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)


async def write_slide_to_disk(folder_name: str, file_name: str, file: UploadFile = File(...)):
    os.mkdir(f"/data/{folder_name}")
    await write_file(folder_name, file_name, file)
    # minio_client.create_object(fr"{folder_name}/{file_name}", file.file.fileno(), file.content_type)
    print("Slide has been saved")
    convert_slide.delay(file_name)


@app.get('')
def test():
    return {"Hello": "World"}


@app.post('/slides')
def create_slide(background_tasks: BackgroundTasks, name: str = Form(...), file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())

    file_name = f"{file_id}.{file.filename.split('.')[1]}"

    try:

        slide_db.insert_slide(CreateSlide(
            slide_id=file_id,
            name=name,
            status=SlideStatus.RUNNING
        ))
        background_tasks.add_task(write_slide_to_disk, file_id, file_name, file=file)
    except Exception as e:
        print(e)

    # file_id = str(uuid.uuid4())
    #
    # file_name = f"{file_id}.{file.filename.split('.')[1]}"
    # try:
    #     add_slide(
    #         name=name,
    #         file_id=file_id,
    #         status='R',
    #     )
    #     background_tasks.add_task(write_slide_to_disk, file_id, file_name, file=file)
    #     return {"Status": "Ok"}
    # except Exception as err:
    #     if err.__class__ == errors.IntegrityError:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="Slide with this name already exists"
    #         )
    #     raise HTTPException(
    #         status_code=500,
    #         detail="Slide couldn't be saved"
    #     )
    pass


@app.get('/slides')
def read_slides():
    slide_db.connection_is_healthy()
    return {"status": "ok"}


@app.delete('/slides/delete/all')
def delete_all():
    minio_client.delete_all_objects()
    return {"status": "ok"}
