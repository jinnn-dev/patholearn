from app.schemas.polygon_data import AnnotationType


def is_info_annotation(annotation_type: AnnotationType) -> bool:
    return annotation_type == AnnotationType.INFO_POINT or annotation_type == AnnotationType.INFO_LINE or annotation_type == annotation_type.INFO_POLYGON
