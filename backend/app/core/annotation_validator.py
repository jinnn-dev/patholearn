from typing import Optional

from shapely.geometry import LineString, LinearRing, Polygon

from app.schemas.polygon_data import AnnotationData, AnnotationType
from app.utils.logger import logger


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
