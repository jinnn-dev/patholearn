from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel


class AnnotationType(IntEnum):
    SOLUTION_POINT = 0
    SOLUTION_LINE = 1
    SOLUTION = 2
    USER_SOLUTION_POINT = 3
    USER_SOLUTION_LINE = 4
    USER_SOLUTION = 5
    BASE = 6,
    SOLUTION_RECT = 7,
    USER_SOLUTION_RECT = 8,
    INFO_POINT = 9,
    INFO_LINE = 10,
    INFO_POLYGON = 11


class Point(BaseModel):
    x: float
    y: float


class AnnotationCoord(BaseModel):
    image: List[Point]


class AnnotationData(BaseModel):
    id: str
    type: AnnotationType
    color: str
    coord: AnnotationCoord
    name: Optional[str]


class RectangleData(AnnotationData):
    width: float
    height: float


class InfoAnnotationData(AnnotationData):
    headerText: str
    detailText: str
    images: Optional[List[str]]


class OffsetRectangleData(RectangleData):
    outerPoints: AnnotationCoord
    innerPoints: AnnotationCoord
    outerOffset: float
    innerOffset: float
    changedManual: bool


class OffsetPolygonData(AnnotationData):
    outerPoints: AnnotationCoord
    innerPoints: AnnotationCoord
    outerOffset: float
    innerOffset: float
    changedManual: bool


class OffsetPointData(AnnotationData):
    offsetImageRadius: float
    offsetRadius: float


class OffsetLineData(AnnotationData):
    outerPoints: AnnotationCoord
    offsetRadius: float
    changedManual: bool
