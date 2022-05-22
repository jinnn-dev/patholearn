from math import hypot

from app.schemas.polygon_data import Point
from app.utils.utils import get_path_length


def test_get_path_length_one():
    points = []
    points.append(Point(x=1, y=0))
    points.append(Point(x=0, y=0))
    assert get_path_length(points) == 1


def test_get_path_length_multiple():
    points = []
    points.append(Point(x=0, y=0))
    points.append(Point(x=0, y=1))
    points.append(Point(x=1, y=1))
    assert get_path_length(points) == 2


def test_get_path_diagonal():
    points = []
    p1 = Point(x=0, y=0)
    p2 = Point(x=1, y=1)
    points.append(p1)
    points.append(p2)
    length = hypot(p1.x - p2.x, p1.y - p2.y)
    assert get_path_length(points) == length
