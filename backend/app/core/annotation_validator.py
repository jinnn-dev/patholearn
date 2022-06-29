from enum import IntEnum
from typing import Optional, Any, List

from pydantic import BaseModel
from shapely.geometry import LineString, LinearRing, Polygon

from app.core.annotation_type import is_info_annotation
from app.schemas.polygon_data import AnnotationData, AnnotationType
from app.schemas.task import TaskType
from app.utils.logger import logger


class ValidationResultType(IntEnum):
    MISSING_NAME = 0
    INVALID_GEOMETRY = 1


class ValidationResult(BaseModel):
    id: str
    result: ValidationResultType


class AnnotationValidator:
    @staticmethod
    def check_if_annotation_is_valid(annotation_data: AnnotationData) -> Optional[bool]:
        annotation = None
        if annotation_data.type == AnnotationType.SOLUTION_LINE:
            annotation = LineString([p.x, p.y] for p in annotation_data.coord.image)
        if annotation_data.type == AnnotationType.SOLUTION:
            annotation = LinearRing([p.x, p.y] for p in annotation_data.coord.image)

        if annotation is not None:
            return annotation.is_valid

        return None

    @staticmethod
    def analyze_polygon_intersection(first: Polygon, second: Polygon) -> Polygon:
        return first.intersection(second)

    @staticmethod
    def validate_annotations(
        annotations: List[Any], task_type: TaskType
    ) -> List[ValidationResult]:
        validation_results = []
        for annotation in annotations:
            annotation_type = annotation["type"]
            if task_type == TaskType.DRAWING_WITH_CLASS:
                if annotation_type == AnnotationType.BASE or is_info_annotation(
                    AnnotationType(annotation_type)
                ):
                    continue
                if "name" not in annotation:
                    validation_results.append(
                        ValidationResult(
                            id=annotation["id"],
                            result=ValidationResultType.MISSING_NAME,
                        )
                    )
        return validation_results
