from fastapi import HTTPException
from app.schema.task import TaskVersion
import requests
from PIL import Image
from app.utils.logger import logger


def get_prediction_to_version(version: TaskVersion, image_data: bytes):
    result = requests.post(
        f"http://10.168.2.83:8080/serve/{version.clearml_id}",
        data=image_data,
        headers={"Content-Type": "image/png"},
    )
    data = result.json()
    if "detail" in data.keys():
        logger.error(data)
        raise HTTPException(status_code=403, detail="Did not work")
    return data["propabilities"][0]
