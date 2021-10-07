from typing import List, Union

from app.core.solver.annotation_analysis import AnnotationAnalysis
from app.core.solver.feeback_generator import FeedbackGenerator
from app.schemas.polygon_data import (AnnotationData, AnnotationType,
                                      OffsetLineData, OffsetPointData,
                                      OffsetPolygonData, OffsetRectangleData,
                                      RectangleData)
from app.schemas.task import Task, TaskFeedback, TaskStatus
from app.utils.colored_printer import ColoredPrinter
from app.utils.timer import Timer
from pydantic import parse_obj_as


class Solver:

    @staticmethod
    def solve(*, user_solution: List[AnnotationData], task: Task) -> TaskFeedback:
        """
        Solves the given user solution to the task and generates feedback for it

        :param user_solution: The solution that should be solved
        :param task: The task with the solution
        :return: The resulting feedback for the
        """
        current_timer = Timer()
        current_timer.start()

        task_result = TaskFeedback(task_id=task.id)
        task_result.result_detail = []
        task_annotation_type = task.annotation_type
        task_solution = task.solution

        if task_solution is None:
            return TaskFeedback(task_id=task.id, task_status=TaskStatus.WRONG,
                                response_text="Es ist keine Musterlösung hinterlegt. Bitte informiere den Kursinhaber.",
                                result_detail=[])

        min_correct = task.min_correct if task.task_type == 0 else len(task.solution)
        should_check_name = False if task.task_type == 0 else True

        if len(user_solution) < min_correct:
            annotation_diff = min_correct - len(user_solution)
            task_result.task_status = TaskStatus.TOO_LESS_INPUTS
            task_result.response_text = f"Es {'fehlt noch eine ' if annotation_diff == 1 else f'fehlen noch {annotation_diff}'} " \
                                        f"{'Annotation' if annotation_diff == 1 else 'Annotationen'}!"

        parsed_user_solution = parse_obj_as(List[Union[RectangleData, AnnotationData]], user_solution)

        if task_annotation_type == AnnotationType.SOLUTION_POINT:
            parsed_task_solution = parse_obj_as(List[OffsetPointData], task_solution)
            solve_result = AnnotationAnalysis.check_point_in_point(user_annotation_data=parsed_user_solution,
                                                                   solution_annotation_data=parsed_task_solution)

            task_result = FeedbackGenerator.generate_point_feedback(solve_result=solve_result, task_result=task_result,
                                                                    min_correct=min_correct,
                                                                    check_name=should_check_name,
                                                                    knowledge_level=task.knowledge_level)

        if task_annotation_type == AnnotationType.SOLUTION_LINE:
            parsed_task_solution = parse_obj_as(List[OffsetLineData], task_solution)
            solve_result = AnnotationAnalysis.check_line_in_line(user_annotation_data=parsed_user_solution,
                                                                 solution_annotation_data=parsed_task_solution)
            task_result = FeedbackGenerator.generate_line_feedback(solve_result=solve_result, task_result=task_result,
                                                                   min_correct=min_correct,
                                                                   check_name=should_check_name,
                                                                   knowledge_level=task.knowledge_level)

        if task_annotation_type == AnnotationType.SOLUTION:
            parsed_task_solution = parse_obj_as(List[Union[OffsetRectangleData, OffsetPolygonData]], task_solution)
            solve_result = AnnotationAnalysis.check_polygon_in_polygon(user_annotation_data=parsed_user_solution,
                                                                       solution_annotation_data=parsed_task_solution)
            task_result = FeedbackGenerator.generate_polygon_feedback(solve_result=solve_result,
                                                                      task_result=task_result, min_correct=min_correct,
                                                                      check_name=should_check_name,
                                                                      knowledge_level=task.knowledge_level)

        current_timer.stop()
        ColoredPrinter.print_lined_info(f"Solver needed {current_timer.total_run_time * 1000}ms")
        return task_result
