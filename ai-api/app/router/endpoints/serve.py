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
import base64

router = APIRouter()


@router.post("/{task_id}/{version_id}")
async def get_prediction(task_id: str, version_id: str, image: UploadFile):
    _, version = await get_task_with_version(task_id, version_id)
    dataset = await get_dataset(dataset_id=version.dataset_id)
    image_data = image.file.read()
    propabilities = get_prediction_to_version(
        version=version,
        image_data=[image_data],
        dataset=dataset,
    )

    if dataset.dataset_type == "classification":
        dataset.metadata.class_map = {
            v: k for k, v in dataset.metadata.class_map.items()
        }

        data = {
            "propabilities": propabilities[0],
            "max_index": propabilities[0].index(max(propabilities[0])),
            "dataset": dataset.metadata,
        }
    else:
        class_map = dataset.metadata.class_map

        label_to_rgb = {}
        for name in class_map.keys():
            color = class_map[name]["color"]
            label_to_rgb[class_map[name]["index"]] = (color[0], color[1], color[2])

        image_bytes = base64.b64decode(propabilities["mask"])
        pred = np.frombuffer(image_bytes, dtype=np.uint8).reshape(
            len(class_map.keys()), propabilities["width"], propabilities["height"]
        )
        composite_mask = np.zeros((pred.shape[1], pred.shape[2], 3), dtype=np.uint8)
        for label, color in label_to_rgb.items():
            channel_mask = pred[label]  # Use label as index
            composite_mask[channel_mask == 1] = color

        image = Image.fromarray(composite_mask).convert("RGB")
        png_stream = BytesIO()
        image.save(png_stream, format="PNG")
        png_stream.seek(0)
        return StreamingResponse(content=png_stream, media_type="image/png")

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
            version=version, image_data=[im_bytes.getvalue()], dataset=dataset
        )
        return True

    except Exception as e:
        logger.error(e)
        return False
