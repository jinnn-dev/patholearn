import math
from typing import List, Tuple, Dict, Union

from shapely.errors import TopologicalError
from shapely.geometry import LineString, Polygon, LinearRing

from app.schemas.polygon_data import AnnotationData, OffsetLineData, OffsetPointData, OffsetPolygonData
from app.schemas.solver_result import LineResult, PointResult, PolygonResult
from app.utils.colored_printer import ColoredPrinter
from app.utils.timer import Timer
from app.utils.utils import get_path_length


class AnnotationAnalysis:
    @staticmethod
    def check_point_in_point(*, user_annotation_data: List[AnnotationData],
                             solution_annotation_data: List[OffsetPointData]) -> Tuple[
        Dict[str, List[PointResult]], List[str]]:
        """
        Test every point in the user annotation with the solution points and generates a solve result.
        Adds every user annotation to the solution annotation with the check results.

        :param user_annotation_data: The point annotations of the user
        :param solution_annotation_data: The point annotations of the solution
        :return: The solve result
        """
        correct_point_ids = {}
        no_match_ids = []
        for user_annotation in user_annotation_data:
            no_match_ids.append(user_annotation.id)
            for solution_annotation in solution_annotation_data:
                if solution_annotation.id not in correct_point_ids:
                    correct_point_ids[solution_annotation.id] = []
                user_point = user_annotation.coord.image[0]
                solution_point = solution_annotation.coord.image[0]
                radius = solution_annotation.offsetImageRadius
                distance = (user_point.x - solution_point.x) ** 2 + (user_point.y - solution_point.y) ** 2

                if distance < radius ** 2:
                    result = PointResult(
                        id=user_annotation.id,
                        distance=math.sqrt(distance),
                        name_matches=False
                    )
                    if user_annotation.name and solution_annotation.name:
                        result.name_matches = user_annotation.name == solution_annotation.name
                    else:
                        result.name_matches = False

                    correct_point_ids.get(solution_annotation.id).append(result)
                    if user_annotation.id in no_match_ids:
                        no_match_ids.remove(user_annotation.id)

        return correct_point_ids, no_match_ids

    @staticmethod
    def check_line_in_line(*, user_annotation_data: List[AnnotationData],
                           solution_annotation_data: List[OffsetLineData]) -> Tuple[
        Dict[str, List[LineResult]], List[str]]:
        """
        Test every line in the user annotation with the solution lines and generates a solve result.
        Adds every user annotation to the solution annotation with the check results.

        :param user_annotation_data: The line annotations of the user
        :param solution_annotation_data: The line annotations of the solution
        :return: The solve result
        """
        correct_line_ids = {}
        no_match_ids = []
        timer = Timer()
        timer.start()

        for user_annotation in user_annotation_data:
            user_line_string = LineString([p.x, p.y] for p in user_annotation.coord.image)
            no_match_ids.append(user_annotation.id)
            for solution_annotation in solution_annotation_data:
                time_before = timer.time_elapsed

                if solution_annotation.id not in correct_line_ids:
                    correct_line_ids[solution_annotation.id] = []

                solution_polygon = Polygon([p.x, p.y] for p in solution_annotation.outerPoints.image)
                percentage_length_difference = user_line_string.length / get_path_length(
                    solution_annotation.coord.image)
                difference = user_line_string.difference(solution_polygon)  # Get those parts of line outside of polygon
                lines_outside = []
                if isinstance(difference, LineString):
                    lines_outside.append(list(difference.coords))
                else:
                    for line in difference:
                        lines_outside.append(list(line.coords))

                annotation_result = LineResult(
                    id=user_annotation.id,
                    name_matches=False,
                    percentage_outside=0.0,
                    intersections=0,
                    percentage_length_difference=percentage_length_difference,
                    lines_outside=lines_outside
                )

                AnnotationAnalysis.__check_name(user_annotation, solution_annotation, annotation_result)

                if difference.is_empty:
                    if user_annotation.id in no_match_ids:
                        no_match_ids.remove(user_annotation.id)
                    correct_line_ids[solution_annotation.id].append(annotation_result)
                if not difference.is_empty and not difference.equals(user_line_string):
                    annotation_result.percentage_outside = difference.length / user_line_string.length
                    if isinstance(difference, LineString):
                        annotation_result.intersections = 1
                    else:
                        annotation_result.intersections = len(difference)
                    if user_annotation.id in no_match_ids:
                        no_match_ids.remove(user_annotation.id)
                    correct_line_ids[solution_annotation.id].append(annotation_result)

                ColoredPrinter.print_lined_info(f"Line analysis needed {(timer.time_elapsed - time_before) * 1000}ms")
        timer.stop()
        ColoredPrinter.print_lined_info(f"Complete Line Check needed: {timer.total_run_time * 1000}ms")
        return correct_line_ids, no_match_ids

    @staticmethod
    def check_polygon_in_polygon(*, user_annotation_data: List[AnnotationData],
                                 solution_annotation_data: List[OffsetPolygonData]) -> Tuple[
        Dict[str, List[PolygonResult]], List[str], List[str]]:
        """
        Test every polygon in the user annotation with the solution polygons and generates a solve result.
        Adds every user annotation to the solution annotation with the check results.

        :param user_annotation_data: The polygon annotations of the user
        :param solution_annotation_data: The polygon annotations of the solution
        :return: The solve result
        """
        correct_polygon_ids = {}
        no_match_ids = []
        invalid_ids = []
        timer = Timer()
        timer.start()

        for user_annotation in user_annotation_data:
            user_polygon = LinearRing([p.x, p.y] for p in user_annotation.coord.image)

            if not user_polygon.is_valid:
                invalid_ids.append(user_annotation.id)
                continue
            no_match_ids.append(user_annotation.id)

            for solution_annotation in solution_annotation_data:

                time_before = timer.time_elapsed

                if solution_annotation.id not in correct_polygon_ids:
                    correct_polygon_ids[solution_annotation.id] = []

                solution_inner_polygon = Polygon([p.x, p.y] for p in solution_annotation.innerPoints.image)
                solution_outer_polygon = Polygon([p.x, p.y] for p in solution_annotation.outerPoints.image)

                if solution_inner_polygon.is_empty:
                    polygon_hole = Polygon(solution_outer_polygon.exterior.coords)
                else:
                    polygon_hole = Polygon(solution_outer_polygon.exterior.coords,
                                           [solution_inner_polygon.exterior.coords])

                percentage_length_difference = user_polygon.length / get_path_length(solution_annotation.coord.image)

                try:
                    hole_difference = user_polygon.difference(polygon_hole)
                    lines_outside = []

                    if not hole_difference.is_empty:
                        if isinstance(hole_difference, LineString):
                            lines_outside.append(list(hole_difference.coords))
                        else:
                            for line in hole_difference:
                                lines_outside.append(list(line.coords))

                    annotation_result = PolygonResult(
                        id=user_annotation.id,
                        name_matches=False,
                        percentage_outside=0.0,
                        intersections=0,
                        percentage_length_difference=percentage_length_difference,
                        percentage_area_difference=Polygon(
                            [p.x, p.y] for p in user_annotation.coord.image).area / Polygon(
                            [p.x, p.y] for p in solution_annotation.coord.image).area,
                        lines_outside=lines_outside
                    )

                    AnnotationAnalysis.__check_name(user_annotation, solution_annotation, annotation_result)

                    if hole_difference.is_empty:
                        if user_annotation.id in no_match_ids:
                            no_match_ids.remove(user_annotation.id)
                        correct_polygon_ids[solution_annotation.id].append(annotation_result)
                    if not hole_difference.is_empty and not hole_difference.equals(user_polygon):
                        annotation_result.percentage_outside = hole_difference.length / user_polygon.length
                        if isinstance(hole_difference, LineString):
                            annotation_result.intersections = 1
                        else:
                            annotation_result.intersections = len(hole_difference)
                        if user_annotation.id in no_match_ids:
                            no_match_ids.remove(user_annotation.id)
                        correct_polygon_ids[solution_annotation.id].append(annotation_result)

                    # ColoredPrinter.print_lined_info(f"Polygon check needed {(timer.time_elapsed - time_before) * 1000}ms")
                except TopologicalError:
                    if user_annotation.id in no_match_ids:
                        no_match_ids.remove(user_annotation.id)
                    invalid_ids.append(user_annotation.id)
        timer.stop()

        # ColoredPrinter.print_lined_info(f"Complete Polygon Check needed {timer.total_run_time * 1000}ms")
        return correct_polygon_ids, no_match_ids, invalid_ids

    @staticmethod
    def __check_name(user_annotation: AnnotationData, solution_annotation: Union[OffsetPolygonData, OffsetLineData],
                     annotation_result: Union[PolygonResult, LineResult]) -> Union[PolygonResult, LineResult]:
        if user_annotation.name and solution_annotation.name:
            annotation_result.name_matches = user_annotation.name == solution_annotation.name
        else:
            annotation_result.name_matches = False
        return annotation_result
