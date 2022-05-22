from typing import Any

from fastapi import APIRouter, Depends, UploadFile, File

from app.api.deps import get_current_active_user
from app.core.polygon_extractor import convert_image_to_annotations
from app.models.user import User


router = APIRouter()


@router.post("/convert")
async def convert_image(
    *,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    contents = await file.read()
    result = convert_image_to_annotations(contents)
    return result
