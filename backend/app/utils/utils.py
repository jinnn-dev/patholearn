import csv
import json
from io import StringIO
from math import hypot
from typing import Any, Dict, Iterator, List, Union

from app.schemas.polygon_data import Point
from app.schemas.solver_result import LineResult, PointResult, PolygonResult
from fastapi import File, UploadFile


def point_diff(p1, p2): return (p1.x - p2.x, p1.y - p2.y)


def get_path_length(vertices: List[Point]) -> float:
    """
    Calculates the length of the given polyline.

    :param vertices: Vertices of the polyline
    :return: The length of the polyline
    """
    differences = (point_diff(p1, p2) for p1, p2 in zip(vertices, vertices[1:]))
    return sum(hypot(*d) for d in differences)


def get_max_value_length(arr_dict: Dict[Any, List[Any]]) -> int:
    """
    Returns the max array length of the items in the dict.

    :param arr_dict: The dict to check
    :return: The max length
    """
    list_of_item_length = [len(v) for k, v in arr_dict.items()]
    if len(list_of_item_length) == 0:
        return 0
    return max(list_of_item_length)


def print_python_dict(matched_ids: Dict[str, List[Union[PointResult, LineResult, PolygonResult]]]):
    """
    Prints dict with different annotation result lists
    """
    result = {}
    for key in matched_ids:
        result[key] = []
        for annotation_result in matched_ids[key]:
            result[key].append(annotation_result.dict())


def get_csv_iterator(csv_file: UploadFile = File(...), skip_headers=False) -> [Iterator, str]:
    """
    Returns an iterator and the csv delimiter for the given file

    :param csv_file: The csv file
    :param skip_headers: Whether the iterator should skip the headers
    :return Iterator and delimiter
    """
    csv_file.file.seek(0)
    csv_reader = csv.reader(StringIO(str(csv_file.file.read(), 'utf-8')))
    headers = next(csv_reader)

    delimiter = ';'
    if '\t' in headers[0]:
        delimiter = '\t'

    csv_file.file.seek(0)
    csv_reader = csv.reader(StringIO(str(csv_file.file.read(), 'utf-8')))

    if skip_headers:
        next(csv_reader)
    return csv_reader, delimiter
