from typing import List

from pydantic import BaseModel

from app.schemas.polygon_data import Point


class ImageDimension(BaseModel):
    height: float
    width: float


class GrayGroup(BaseModel):
    gray_value: int
    annotations: List[List[Point]]


class ExtractionResult(BaseModel):
    image: ImageDimension
    annotations: List[GrayGroup]
