from typing import List, Union

from pydantic import parse_obj_as

from app.core.solver.annotation_analysis import AnnotationAnalysis
from app.core.solver.feeback_generator import FeedbackGenerator
from app.core.solver.select_images_analysis import SelectImagesAnalysis
from app.schemas.polygon_data import (
    AnnotationData,
    AnnotationType,
    OffsetLineData,
    OffsetPointData,
    OffsetPolygonData,
    OffsetRectangleData,
    RectangleData,
)
from app.schemas.task import Task, TaskFeedback, TaskStatus, TaskType
from app.schemas.user_solution import UserSolution
from app.utils.logger import logger
from app.utils.timer import Timer


class Solver:
    @staticmethod
    def solve(*, user_solution: UserSolution, task: Task) -> TaskFeedback:
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
        if not task.can_be_solved:
            return TaskFeedback(
                task_id=task.id,
                task_status=TaskStatus.CORRECT,
                response_text="Danke für das Einreichen",
                result_detail=[],
            )

        if task_solution is None:
            return TaskFeedback(
                task_id=task.id,
                task_status=TaskStatus.WRONG,
                response_text="Es ist keine Musterlösung hinterlegt. Bitte informiere den Kursinhaber.",
                result_detail=[],
            )

        if task.task_type == TaskType.IMAGE_SELECT:
            solution_data = task.solution
            user_solution_data = (
                []
                if user_solution.solution_data is None
                else user_solution.solution_data
            )
            correct_images, wrong_images = SelectImagesAnalysis.check_select_images(
                task_solution=solution_data, user_solution=user_solution_data
            )

            task_result = FeedbackGenerator.generate_image_select_feedback(
                task_feedback=task_result,
                correct_image_indices=correct_images,
                wrong_image_indices=wrong_images,
                solution_data=solution_data,
            )
        else:
            min_correct = (
                task.min_correct if task.task_type == 0 else len(task.solution)
            )
            should_check_name = False if task.task_type == 0 else True
            if len(user_solution.solution_data) == 0:
                task_result.task_status = TaskStatus.TOO_LESS_INPUTS
                task_result.response_text = "Deine Lösung enthält keine Annotationen"
                return task_result

            user_solution_data = user_solution.solution_data
            if len(user_solution_data) < min_correct:
                annotation_diff = min_correct - len(user_solution_data)
                task_result.task_status = TaskStatus.TOO_LESS_INPUTS
                task_result.response_text = (
                    f"Es {'fehlt noch eine ' if annotation_diff == 1 else f'fehlen noch {annotation_diff}'} "
                    f"{'Annotation' if annotation_diff == 1 else 'Annotationen'}!"
                )

            parsed_user_solution = parse_obj_as(
                List[Union[RectangleData, AnnotationData]], user_solution_data
            )

            if task_annotation_type == AnnotationType.SOLUTION_POINT:
                parsed_task_solution = parse_obj_as(
                    List[OffsetPointData], task_solution
                )
                solve_result = AnnotationAnalysis.check_point_in_point(
                    user_annotation_data=parsed_user_solution,
                    solution_annotation_data=parsed_task_solution,
                )

                task_result = FeedbackGenerator.generate_point_feedback(
                    solve_result=solve_result,
                    task_result=task_result,
                    min_correct=min_correct,
                    check_name=should_check_name,
                    knowledge_level=task.knowledge_level,
                )

            if task_annotation_type == AnnotationType.SOLUTION_LINE:
                parsed_task_solution = parse_obj_as(List[OffsetLineData], task_solution)
                solve_result = AnnotationAnalysis.check_line_in_line(
                    user_annotation_data=parsed_user_solution,
                    solution_annotation_data=parsed_task_solution,
                )
                task_result = FeedbackGenerator.generate_line_feedback(
                    solve_result=solve_result,
                    task_result=task_result,
                    min_correct=min_correct,
                    check_name=should_check_name,
                    knowledge_level=task.knowledge_level,
                )

            if task_annotation_type == AnnotationType.SOLUTION:
                parsed_task_solution = parse_obj_as(
                    List[Union[OffsetRectangleData, OffsetPolygonData]], task_solution
                )
                solve_result = AnnotationAnalysis.check_polygon_in_polygon(
                    user_annotation_data=parsed_user_solution,
                    solution_annotation_data=parsed_task_solution,
                )
                task_result = FeedbackGenerator.generate_polygon_feedback(
                    solve_result=solve_result,
                    task_result=task_result,
                    min_correct=min_correct,
                    check_name=should_check_name,
                    knowledge_level=task.knowledge_level,
                )

        current_timer.stop()
        logger.debug(f"Solver needed {current_timer.total_run_time * 1000}ms")
        return task_result
