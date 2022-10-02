from typing import Any, List

from fastapi import APIRouter, Depends, UploadFile, File, Form
from shapely.geometry import Polygon

from app.api.deps import get_current_active_superuser
from app.core.annotation_extractor import extract_annotations_from_image
from app.core.annotation_validator import AnnotationValidator
from app.models.user import User
from app.schemas.extractor import (
    ExtractionResult,
    ExtractionResultList,
    GreyGroupSummary,
)
from app.utils.logger import logger

router = APIRouter()


@router.post("/convert")
async def convert_image(
    *,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    contents = await file.read()
    result = extract_annotations_from_image(file.filename, contents)
    return result


@router.post("/convertMultiple")
async def convert_image(
    *,
    images: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    logger.debug("convert multiple files")
    logger.debug([image.filename for image in images])

    extraction_results: List[ExtractionResult] = []

    grey_values = {}

    for image in images:
        extraction_result = extract_annotations_from_image(
            image.filename, image.file.read()
        )
        extraction_results.append(extraction_result)

        for grey_group in extraction_result.grey_groups:
            if grey_group.grey_value in grey_values:
                grey_values[grey_group.grey_value].annotation_count += 1
            else:
                grey_values[grey_group.grey_value] = GreyGroupSummary(
                    grey_value=grey_group.grey_value,
                    annotation_count=0,
                    annotation_group=grey_group.annotation_group,
                )
    return ExtractionResultList(
        summary=list(grey_values.values()), results=extraction_results
    )
