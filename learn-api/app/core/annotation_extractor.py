from typing import Union, List

import cv2.cv2
import imutils
import numpy as np
from imutils import contours

from app.schemas.extractor import GreyGroup, ExtractionResult, ImageDimension
from app.schemas.task import AnnotationData, OffsetPolygonData, AnnotationGroup
from app.schemas.polygon_data import Point
from app.schemas.task import AnnotationGroup
from app.utils.logger import logger
from app.utils.timer import Timer


def extract_annotations_from_image(
    file_name: str, file_contents: Union[bytes, str]
) -> ExtractionResult:
    """
    Extracts all polygons grouped by gray values of the given file contents.

    :param file_name: Name of the file
    :param file_contents: Content of a file

    :return: Conversion result
    """
    timer = Timer()
    timer.start()

    np_arr = np.fromstring(file_contents, np.uint8)
    img_gray = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

    time = timer.time_elapsed
    logger.debug(f"Loading image into cv2 took {timer.time_elapsed}s")

    annotation_count = 0

    hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
    available_gray_values = np.unique(np.nonzero(hist))
    available_gray_values = available_gray_values[available_gray_values != 0]
    time_hist = timer.time_elapsed
    logger.debug(f"Calculating Histogram took {timer.time_elapsed - time}s")
    annotation_groups = []

    for grey_value in available_gray_values:
        img_mask = cv2.inRange(img_gray, np.array(grey_value), np.array(grey_value))
        found_contours = cv2.findContours(
            img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        found_contours = imutils.grab_contours(found_contours)
        (found_contours, _) = contours.sort_contours(found_contours)
        annotations = []
        for contour in found_contours:
            size = cv2.contourArea(contour)
            corners = cv2.approxPolyDP(
                contour, 0.004 * cv2.arcLength(contour, True), True
            )  # Uses Douglas-Peucker algorithm
            corners = corners.ravel()
            if (
                len(corners) > 2 and size > 200.0
            ):  # Maybe use different Threshold for robuster noise removal
                annotation = []
                for x, y in zip(corners[0::2], corners[1::2]):
                    annotation.append(Point(x=float(x), y=float(y)))
                annotations.append(annotation)
        annotation_count += len(annotations)
        annotation_groups.append(
            GreyGroup(
                grey_value=int(grey_value),
                annotations=annotations,
                annotation_group=AnnotationGroup(
                    name=str(grey_value), color="#" + str(grey_value) * 6
                ),
            )
        )
    logger.debug(f"Feature extraction took {timer.time_elapsed - time_hist}s")
    timer.stop()
    logger.debug(f"Annotation extraction took {timer.total_run_time}s")

    height, width = img_gray.shape
    return ExtractionResult(
        image=ImageDimension(height=height, width=width),
        annotation_count=annotation_count,
        file_name=file_name,
        grey_groups=annotation_groups,
    )


def create_mask_from_annotations(
    annotations: List[OffsetPolygonData],
    annotation_groups: List[AnnotationGroup],
    slide_width: int,
    slide_height: int,
):
    logger.debug(slide_width)
    logger.debug(slide_height)
    logger.debug(annotation_groups)
    annotations_to_group: List[OffsetPolygonData] = []

    # for group in annotation_groups:
    #     annotations_to_group.append(
    #         [annotation for annotation in annotations if annotation.name == group.name]
    #     )
    timer = Timer()
    timer.start()
    # logger.info("Creating base image")
    mask_base = np.zeros((slide_height, slide_width, 3), dtype=np.uint8)
    # logger.info(timer.checkpoint_time())
    # logger.info(f"Creating base image done in {timer.checkpoint_time()}s")
    # logger.info("Going over annotations")
    for index, annotation in enumerate(annotations):
        points = annotation.coord.image
        group = next(
            group for group in annotation_groups if group.name == annotation.name
        )
        # prefix = f"[{index}/{len(annotations)}]"
        # logger.info(f"{prefix} Parsing points array")
        parsed_points = []
        for point in points:
            parsed_points.append([int(point.x), int(point.y)])
        # logger.info(f"{prefix} Done parsing in {timer.checkpoint_time()}s")
        np_points = np.array(parsed_points, dtype=np.int32)
        # logger.info(f"{prefix} Done creating numpy array in {timer.checkpoint_time()}s")
        color = tuple(int(group.color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        mask_base = cv2.fillPoly(mask_base, pts=[np_points], color=color[::-1])
        # logger.info(f"{prefix} Done creating polygon in {timer.checkpoint_time()}s")

    _, mask = cv2.imencode(".png", mask_base)
    logger.info(f"Done encoding image in {timer.checkpoint_time()}s")
    timer.stop()
    return mask.tobytes()
