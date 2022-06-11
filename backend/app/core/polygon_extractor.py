from typing import Union

import cv2.cv2
import imutils
import numpy as np
from imutils import contours

from app.schemas.extractor import GrayGroup, ExtractionResult, ImageDimension
from app.schemas.polygon_data import Point
from app.utils.logger import logger
from app.utils.timer import Timer


def convert_image_to_annotations(file_contents: Union[bytes, str]) -> ExtractionResult:
    """
    Extracts all polygons grouped by gray values of the given file contents.

    :param file_contents: Content of a file
    :return: Conversion result
    """
    timer = Timer()
    timer.start()

    np_arr = np.fromstring(file_contents, np.uint8)
    img_gray = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

    time = timer.time_elapsed
    logger.debug(f"Loading image into cv2 took {timer.time_elapsed}s")

    hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
    available_gray_values = np.unique(np.nonzero(hist))
    available_gray_values = available_gray_values[available_gray_values != 0]
    time_hist = timer.time_elapsed
    logger.debug(f"Calculating Histogram took {timer.time_elapsed - time}s")
    annotation_groups = []

    for gray_value in available_gray_values:
        img_mask = cv2.inRange(img_gray, np.array(gray_value), np.array(gray_value))
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
        annotation_groups.append(
            GrayGroup(gray_value=int(gray_value), annotations=annotations)
        )
    logger.debug(f"Feature extraction took {timer.time_elapsed - time_hist}s")
    timer.stop()
    logger.debug(f"Annotation extraction took {timer.total_run_time}s")

    height, width = img_gray.shape
    return ExtractionResult(
        image=ImageDimension(height=height, width=width), annotations=annotation_groups
    )
