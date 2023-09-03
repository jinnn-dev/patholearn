from fastapi import HTTPException
from app.schema.task import TaskVersion
import requests
from PIL import Image
from app.utils.logger import logger
from app.schema.dataset import Dataset
import json
import base64
from PIL import Image
from io import BytesIO
from typing import List


def get_prediction_to_version(
    version: TaskVersion, image_data: List[bytes], dataset: Dataset
):
    encoded_images = []
    for image in image_data:
        encoded_images.append(base64.b64encode(image).decode())
    metadata = dataset.metadata.dict()

    result = requests.post(
        f"http://10.168.2.83:8080/serve/{version.clearml_id}",
        json={"image": encoded_images, "metadata": metadata},
        headers={"Content-Type": "application/json"},
    )
    data = result.json()
    if "detail" in data.keys():
        logger.error(data)
        raise HTTPException(status_code=403, detail="Did not work")
    return data["propabilities"]


def remove_prediction_endpoint(version: TaskVersion):
    pass
