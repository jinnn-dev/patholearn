from math import hypot
from typing import List, Dict, Any

from app.schemas.polygon_data import Point

point_diff = lambda p1, p2: (p1.x - p2.x, p1.y - p2.y)


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
