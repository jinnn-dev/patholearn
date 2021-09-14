from typing import Tuple, List, Optional

from pydantic import BaseModel


class SolverResultBase(BaseModel):
    id: str
    name_matches: bool
    error: Optional[bool] = False


class PointResult(SolverResultBase):
    distance: float


class LineResult(SolverResultBase):
    percentage_outside: float
    intersections: int
    percentage_length_difference: float
    lines_outside: List[List[Tuple[float, float]]]


class PolygonResult(LineResult):
    percentage_area_difference: float
