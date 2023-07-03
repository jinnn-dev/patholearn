from shutil import unpack_archive
from typing import Any, BinaryIO, Callable, ParamSpec
import glob
import os
from celery import Celery

from clearml import Dataset as ClearmlDataset
from asgiref.sync import async_to_sync
from fastapi import UploadFile
from PIL import Image

from app.crud.dataset import update_dataset, update_dataset_status
from app.utils.io import (
    delete_folder,
    delete_osx_files,
    write_temporary_file,
    contains_subdirectory,
)
from app.schema.dataset import Dataset
from app.clearml_wrapper.clearml_wrapper import (
    add_files_to_dataset,
    create_dataset as create_clearml_dataset,
    finalize_dataset,
    set_metadata_of_dataset,
)
from app.utils.logger import logger

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "amqp://guest:guest@rabbit:5673//"
)

P = ParamSpec("P")


def create_dataset_backgroud(dataset: Dataset, file: BinaryIO):
    try:
        create_dataset(dataset, file)
    except Exception as error:
        logger.exception(f"Failed creating dataset: {error}")


def create_dataset(dataset: Dataset, file: BinaryIO):
    temp_file_path = write_temporary_file(file=file, file_type="zip")
    result = celery_app.send_task(
        name="create_dataset",
        args=[temp_file_path, str(dataset.id)],
        retries=3,
        queue="ai_api",
    )
    logger.debug(result)


def parse_extracted_folder(folder_path: str):
    for folder in glob.glob(folder_path + "/*"):
        if contains_subdirectory(folder):
            logger.debug(folder)
            raise ValueError("Folder contains subdirectories")
    class_map = {}
    class_index = 0
    classes = []
    x = None
    y = None
    for dir in os.listdir(folder_path):
        if dir not in class_map:
            if x is None:
                image = glob.glob(os.path.join(folder_path, dir, "*.*"))[0]
                logger.info(image)
                im = Image.open(image)
                width, height = im.size
                x = width
                y = height
            class_map[dir] = class_index
            classes.append(class_index)
            class_index += 1

    return {"class_map": class_map, "classes": classes, "dimension": {"x": x, "y": y}}
