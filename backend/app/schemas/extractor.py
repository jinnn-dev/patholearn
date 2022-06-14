from typing import List, Optional

from pydantic import BaseModel

from app.schemas.polygon_data import Point
from app.schemas.task import AnnotationGroup


class ImageDimension(BaseModel):
    height: float
    width: float


class GreyGroup(BaseModel):
    grey_value: int
    annotations: List[List[Point]]
    annotation_group: Optional[AnnotationGroup]


class ExtractionResult(BaseModel):
    file_name: str
    image: ImageDimension
    annotation_count: int
    grey_groups: List[GreyGroup]


class GreyGroupSummary(BaseModel):
    grey_value: int
    annotation_count: int
    annotation_group: Optional[AnnotationGroup]


class ExtractionResultList(BaseModel):
    summary: List[GreyGroupSummary]
    results: List[ExtractionResult]
