from fastapi import APIRouter, UploadFile, Response, HTTPException
from starlette.responses import StreamingResponse
import requests
from app.utils.logger import logger
from PIL import Image
import numpy as np
from io import BytesIO
from clearml import Task as ClearmlTask, Model
from app.crud.task import get_task_with_version
from app.crud.dataset import get_dataset
from app.schema.task import TaskVersion, Task
from app.core.serve.prediction import get_prediction_to_version

router = APIRouter()


@router.post("/{task_id}/{version_id}")
async def get_prediction(task_id: str, version_id: str, image: UploadFile):
    _, version = await get_task_with_version(task_id, version_id)
    dataset = await get_dataset(dataset_id=version.dataset_id)
    propabilities = get_prediction_to_version(
        version=version, image_data=image.file.read(), dataset=dataset
    )
    dataset.metadata.class_map = {v: k for k, v in dataset.metadata.class_map.items()}

    data = {
        "propabilities": propabilities,
        "max_index": propabilities.index(max(propabilities)),
        "dataset": dataset.metadata,
    }
    return data


@router.get("/{task_id}/{version_id}")
async def get_serving(task_id: str, version_id: str):
    _, version = await get_task_with_version(task_id, version_id)
    dataset = await get_dataset(dataset_id=version.dataset_id)

    try:
        if dataset.metadata.is_grayscale:
            imarray = np.random.rand(100, 100) * 255
        else:
            imarray = (
                np.random.rand(100, 100, 1 if dataset.metadata.is_grayscale else 3)
                * 255
            )
        im = Image.fromarray(imarray.astype("uint8")).convert("RGBA")
        im_bytes = BytesIO()
        im.save(im_bytes, "PNG")
        get_prediction_to_version(
            version=version, image_data=im_bytes.getvalue(), dataset=dataset
        )
        return True

    except Exception as e:
        logger.error(e)
        return False
