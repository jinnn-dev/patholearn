from enum import IntEnum
from typing import Optional, Any, List

from pydantic import BaseModel
from shapely.geometry import LineString, LinearRing, Polygon

from app.core.annotation_type import is_info_annotation, get_geometry_to_annotation_type
from app.schemas.polygon_data import AnnotationData, AnnotationType
from app.schemas.task import TaskType
from app.utils.logger import logger


class ValidationResultType(IntEnum):
    MISSING_NAME = 0
    INVALID_GEOMETRY = 1


class ValidationResult(BaseModel):
    id: str
    result: List[ValidationResultType]


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
    def is_geometry_valid(annotation: AnnotationData) -> bool:
        geometry = get_geometry_to_annotation_type(annotation)
        return geometry.is_valid

    @staticmethod
    def validate_annotations(
        annotations: List[AnnotationData], task_type: TaskType
    ) -> List[ValidationResult]:
        validation_results = []
        for annotation in annotations:
            annotation_type = annotation.type
            validation_result_types: List[ValidationResultType] = []

            if not AnnotationValidator.is_geometry_valid(annotation):
                validation_result_types.append(ValidationResultType.INVALID_GEOMETRY)
            if task_type == TaskType.DRAWING_WITH_CLASS:
                if annotation_type == AnnotationType.BASE:
                    continue
                if (
                    annotation.name is None
                    and is_info_annotation(annotation.type) is False
                ):
                    validation_result_types.append(ValidationResultType.MISSING_NAME)

            if len(validation_result_types) > 0:
                validation_results.append(
                    ValidationResult(id=annotation.id, result=validation_result_types)
                )
        logger.info(validation_results)
        return validation_results
