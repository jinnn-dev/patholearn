from fastapi import APIRouter, UploadFile, Response
from starlette.responses import StreamingResponse
import requests
from app.utils.logger import logger
from PIL import Image
import numpy as np
from io import BytesIO

router = APIRouter()


@router.post("")
async def get_prediction(image: UploadFile):
    result = requests.post(
        "http://10.168.2.83:8080/serve/segmentation",
        data=image.file.read(),
        headers={"Content-Type": "image/png"},
    )
    data = result.json()
    mask = np.asarray(data["mask"][0])

    if mask.shape[0] == 1:
        mask = np.squeeze(mask)
        print(mask.min())
        mask = np.clip(mask, 0, np.inf)
        mask[mask > 0] = 1
        mask = (mask * 255).astype(np.uint8)

    img = Image.fromarray(mask)
    membuf = BytesIO()
    img.save(membuf, format="png")
    membuf.seek(0)
    return StreamingResponse(membuf, media_type="image/png")
