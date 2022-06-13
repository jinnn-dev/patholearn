from typing import Any, List

from fastapi import APIRouter, Depends, UploadFile, File

from app.api.deps import get_current_active_superuser
from app.core.polygon_extractor import convert_image_to_annotations
from app.models.user import User


router = APIRouter()


@router.post("/convert")
async def convert_image(
    *,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    contents = await file.read()
    result = convert_image_to_annotations(contents)
    return result


@router.post("/convertMultiple")
async def convert_image(
    *,
    images: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    # logger.info()
    return None
