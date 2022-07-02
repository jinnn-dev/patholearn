from shapely.geometry import LinearRing, LineString, Point
from shapely.geometry.base import BaseGeometry

from app.schemas.polygon_data import AnnotationType, AnnotationData


def is_info_annotation(annotation_type: AnnotationType) -> bool:
    return (
        annotation_type == AnnotationType.INFO_POINT
        or annotation_type == AnnotationType.INFO_LINE
        or annotation_type == annotation_type.INFO_POLYGON
    )


def is_polygon(annotation_type: AnnotationType) -> bool:
    return (
        annotation_type == AnnotationType.SOLUTION
        or annotation_type == AnnotationType.USER_SOLUTION
        or annotation_type == AnnotationType.INFO_POLYGON
    )


def is_line(annotation_type: AnnotationType) -> bool:
    return (
        annotation_type == AnnotationType.SOLUTION_LINE
        or annotation_type == AnnotationType.USER_SOLUTION_LINE
        or annotation_type == AnnotationType.INFO_LINE
    )


def get_geometry_to_annotation_type(annotation_data: AnnotationData) -> BaseGeometry:
    if is_polygon(annotation_data.type):
        annotation = LinearRing([p.x, p.y] for p in annotation_data.coord.image)
    elif is_line(annotation_data.type):
        annotation = LineString([p.x, p.y] for p in annotation_data.coord.image)
    else:
        coord = annotation_data.coord.image[0]
        annotation = Point(coord.x, coord.y)
    return annotation
