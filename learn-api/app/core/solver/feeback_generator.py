from typing import Dict, List, Tuple, Union

from app.core.solver.feedback_config import FeedbackConfig
from app.core.solver.task_result_factory import TaskResultFactory
from app.schemas.solver_result import LineResult, PointResult, PolygonResult
from app.schemas.task import (
    AnnotationFeedback,
    SelectImageFeedback,
    TaskFeedback,
    TaskStatus,
)
from app.utils.utils import get_max_value_length


class FeedbackGenerator:
    """
    Offers methods for generating feedback for different annotations types
    """

    @staticmethod
    def generate_point_feedback(
        *,
        solve_result: Tuple[Dict[str, List[PointResult]], List[str]],
        task_result: TaskFeedback,
        min_correct: int,
        knowledge_level: int,
        check_name: bool = False,
    ) -> TaskFeedback:
        """
        Generates feedback for a solve result with point annotations

        :param solve_result: Result of a Task
        :param task_result: TaskResult object
        :param min_correct: The minimum annotations that have to be correct
        :param knowledge_level: The knowledge level ot the task
        :param check_name: If the annotation name should be checked
        :return: The resulting Feedback
        """
        FeedbackGenerator.__generate_no_match_feedback(task_result, solve_result[1])

        matched_ids = FeedbackGenerator.__filter_best_match(
            solve_result[0], key="distance"
        )
        no_match_ids = solve_result[1]

        most_matches_value = get_max_value_length(matched_ids)

        if most_matches_value == 0:
            return TaskResultFactory.wrong_status(task_result)

        if most_matches_value == 0 and len(no_match_ids) == 0:
            return TaskResultFactory.wrong_name_status(task_result)

        correct_count = 0
        for key in matched_ids:
            for annotation in matched_ids[key]:
                if len(matched_ids[key]) > 1:
                    TaskResultFactory.append_result_detail(
                        annotation_id=annotation.id,
                        status=TaskStatus.DUPLICATE_HIT,
                        percentage=0.0,
                        task_result=task_result,
                    )
                    if task_result.task_status is None:
                        TaskResultFactory.partial_status(task_result)
                else:
                    if check_name:

                        if not annotation.name_matches:
                            status = TaskStatus.WRONG_NAME
                            if knowledge_level == 2:
                                status = TaskStatus.WRONG
                            TaskResultFactory.append_result_detail(
                                annotation_id=annotation.id,
                                status=status,
                                percentage=1.0,
                                task_result=task_result,
                            )
                        else:
                            correct_count += 1
                            TaskResultFactory.append_result_detail(
                                annotation_id=annotation.id,
                                status=TaskStatus.CORRECT,
                                percentage=1.0,
                                task_result=task_result,
                            )
                    else:
                        correct_count += 1
                        TaskResultFactory.append_result_detail(
                            annotation_id=annotation.id,
                            status=TaskStatus.CORRECT,
                            percentage=1.0,
                            task_result=task_result,
                        )

        if not task_result.task_status:
            if correct_count >= min_correct:
                TaskResultFactory.correct_status(task_result)
            else:
                TaskResultFactory.partial_status(task_result)
        return task_result

    @staticmethod
    def generate_line_feedback(
        *,
        solve_result: Tuple[Dict[str, List[LineResult]], List[str]],
        task_result: TaskFeedback,
        min_correct: int,
        knowledge_level: int,
        check_name: bool = False,
    ) -> TaskFeedback:
        """
        Generates feedback for a solve result with line annotations

        :param solve_result: Result of a Task
        :param task_result: TaskResult object
        :param min_correct: The minimum annotations that have to be correct
        :param knowledge_level: The knowledge level ot the task
        :param check_name: If the annotation name should be checked
        :return: The resulting Feedback
        """
        FeedbackGenerator.__generate_no_match_feedback(task_result, solve_result[1])

        matched_ids = FeedbackGenerator.__filter_best_match(
            solve_result[0], key="percentage_outside"
        )
        no_match_ids = solve_result[1]
        most_matches_values = get_max_value_length(matched_ids)

        if most_matches_values == 0 and len(no_match_ids) == 0:
            return TaskResultFactory.wrong_status(task_result)

        correct_count = 0
        for key in matched_ids:
            for annotation in matched_ids[key]:

                if knowledge_level != 0:
                    annotation.lines_outside = []

                if len(matched_ids[key]) > 1:
                    TaskResultFactory.append_result_detail(
                        annotation_id=annotation.id,
                        status=TaskStatus.DUPLICATE_HIT,
                        percentage=1.0,
                        task_result=task_result,
                    )
                else:
                    task_result_detail = FeedbackGenerator.generate_detail_line_result(
                        annotation, check_name, knowledge_level
                    )
                    task_result.result_detail.append(task_result_detail)
                    if task_result_detail.status == TaskStatus.CORRECT:
                        correct_count += 1

        if not task_result.task_status:
            if correct_count < min_correct:
                task_result.task_status = TaskStatus.WRONG
                task_result.response_text = (
                    "Einige Annotationen sind noch nicht ganz richtig!"
                )
            else:
                TaskResultFactory.correct_status(task_result)

        return task_result

    @staticmethod
    def generate_polygon_feedback(
        *,
        solve_result: Tuple[Dict[str, List[PolygonResult]], List[str], List[str]],
        task_result: TaskFeedback,
        min_correct: int,
        knowledge_level: int,
        check_name: bool = False,
    ) -> TaskFeedback:
        """
        Generates feedback for a solve result with polygon annotations

        :param solve_result: Result of a Task
        :param task_result: TaskResult object
        :param min_correct: The minimum annotations that have to be correct
        :param knowledge_level: The knowledge level ot the task
        :param check_name: If the annotation name should be checked
        :return: The resulting Feedback
        """

        matched_ids, no_match_ids, invalid_ids = solve_result

        FeedbackGenerator.__generate_no_match_feedback(task_result, no_match_ids)

        FeedbackGenerator.__generate_invalid_feedback(task_result, invalid_ids)

        # Filter best match if polygon hits multiple solution polygons
        matched_ids = FeedbackGenerator.__get_best_match_duplicate_hit(
            matched_ids, key="percentage_outside"
        )

        most_matches_values = get_max_value_length(matched_ids)

        if most_matches_values == 0 and len(no_match_ids) == 0:
            return TaskResultFactory.wrong_status(task_result)

        correct_count = 0

        for solution_id in matched_ids:
            if len(matched_ids[solution_id]) > 1:
                area_percentage_sum = 0
                for user_annotation in matched_ids[solution_id]:
                    if user_annotation.percentage_outside > 0.1:
                        TaskResultFactory.append_result_detail(
                            annotation_id=user_annotation.id,
                            status=TaskStatus.WRONG,
                            percentage=0.0,
                            task_result=task_result,
                        )
                        matched_ids[solution_id].remove(user_annotation)
                    else:
                        area_percentage_sum += (
                            user_annotation.percentage_area_difference
                        )

                for user_annotation in matched_ids[solution_id]:
                    lower_border = FeedbackConfig.get_weighted_border(
                        border=FeedbackConfig.LOWER_AREA_BORDER,
                        knowledge_level=knowledge_level,
                    )
                    upper_border = FeedbackConfig.get_weighted_border(
                        border=FeedbackConfig.UPPER_AREA_BORDER,
                        knowledge_level=knowledge_level,
                    )

                    if lower_border < area_percentage_sum < upper_border:
                        if check_name:
                            if FeedbackGenerator.__generate_name_feedback(
                                user_annotation=user_annotation,
                                percentage=area_percentage_sum,
                                task_feedback=task_result,
                                knowledge_level=knowledge_level,
                            ):
                                correct_count += 1
                        else:
                            TaskResultFactory.append_result_detail(
                                annotation_id=user_annotation.id,
                                status=TaskStatus.CORRECT,
                                percentage=area_percentage_sum,
                                task_result=task_result,
                            )
                            correct_count += 1
                    else:
                        TaskResultFactory.append_result_detail(
                            annotation_id=user_annotation.id,
                            status=TaskStatus.WRONG,
                            percentage=area_percentage_sum,
                            task_result=task_result,
                        )
            else:
                for user_annotation in matched_ids[solution_id]:
                    if knowledge_level != 0:
                        user_annotation.lines_outside = []

                    task_result_detail = (
                        FeedbackGenerator.generate_detail_polygon_result(
                            user_annotation, check_name, knowledge_level
                        )
                    )

                    task_result.result_detail.append(task_result_detail)
                    if task_result_detail.status == TaskStatus.CORRECT:
                        correct_count += 1

        if not task_result.task_status:
            if correct_count < min_correct:
                TaskResultFactory.wrong_status(task_result)
                task_result.response_text = "Einige Annotationen stimmen noch nicht"
            else:
                TaskResultFactory.correct_status(task_result)

        return task_result

    @staticmethod
    def generate_detail_line_result(
        line_result: LineResult, check_name: bool, knowledge_level: int
    ) -> AnnotationFeedback:
        """
        Generates a feedback result for the given line annotation result

        :param line_result: The result of the line annotation check
        :param check_name: If feedback should be generated for the line name or not
        :param knowledge_level: The knowledge level ot the task
        :return: The feedback result
        """
        annotation_result = AnnotationFeedback(id=line_result.id)
        percentage_length_difference = line_result.percentage_length_difference
        percentage_outside = line_result.percentage_outside

        length_border = FeedbackConfig.get_weighted_border(
            border=FeedbackConfig.PERCENTAGE_LENGTH_DIFFERENCE,
            knowledge_level=knowledge_level,
            decent_value=0.2,
        )

        percentage_outside_border = FeedbackConfig.get_weighted_border(
            border=FeedbackConfig.PERCENTAGE_OUTSIDE,
            knowledge_level=knowledge_level,
            decent_value=0.02,
        )

        if percentage_length_difference < length_border:
            annotation_result.status = TaskStatus.WRONG
            annotation_result.percentage = percentage_length_difference
        elif line_result.percentage_outside >= percentage_outside_border:
            annotation_result.status = TaskStatus.INACCURATE
            annotation_result.percentage = 1.0 - percentage_outside
        elif check_name and not line_result.name_matches:
            annotation_result.status = TaskStatus.WRONG_NAME
            annotation_result.percentage = 1.0 - percentage_outside
        elif line_result.intersections == 0:
            annotation_result.status = TaskStatus.CORRECT
            annotation_result.percentage = 1.0
        else:
            annotation_result.status = TaskStatus.CORRECT
            annotation_result.percentage = 1.0 - percentage_outside
        annotation_result.lines_outside = line_result.lines_outside

        if annotation_result.status == TaskStatus.INACCURATE and knowledge_level != 0:
            annotation_result.status = TaskStatus.WRONG

        if annotation_result.status == TaskStatus.WRONG_NAME and knowledge_level == 2:
            annotation_result.status = TaskStatus.WRONG

        return annotation_result

    @staticmethod
    def generate_detail_polygon_result(
        polygon_result: PolygonResult, check_name: bool, knowledge_level: int
    ) -> AnnotationFeedback:
        """
        Generates a feedback result for the given polygon annotation result

        :param knowledge_level:
        :param polygon_result: The result of the polygon annotation check
        :param check_name: If feedback should be generated for the polygon name or not
        :param knowledge_level: The knowledge level ot the task
        :return: The feedback result
        """
        annotation_result = AnnotationFeedback(id=polygon_result.id)
        percentage_length_difference = polygon_result.percentage_length_difference
        percentage_outside = polygon_result.percentage_outside

        length_border = FeedbackConfig.get_weighted_border(
            border=FeedbackConfig.PERCENTAGE_LENGTH_DIFFERENCE,
            knowledge_level=knowledge_level,
            decent_value=0.2,
        )

        percentage_outside_border = FeedbackConfig.get_weighted_border(
            border=FeedbackConfig.PERCENTAGE_OUTSIDE,
            knowledge_level=knowledge_level,
            decent_value=0.02,
        )
        if percentage_length_difference < length_border:
            annotation_result.status = TaskStatus.WRONG
            annotation_result.percentage = percentage_length_difference
        elif percentage_outside >= percentage_outside_border:
            annotation_result.status = TaskStatus.INACCURATE
            annotation_result.percentage = 1.0 - percentage_outside
        elif check_name and not polygon_result.name_matches:
            annotation_result.status = TaskStatus.WRONG_NAME
            annotation_result.percentage = 1.0 - percentage_outside
        else:
            annotation_result.status = TaskStatus.CORRECT
            annotation_result.percentage = 1.0 - percentage_outside
        annotation_result.lines_outside = polygon_result.lines_outside

        if annotation_result.status == TaskStatus.INACCURATE and knowledge_level != 0:
            annotation_result.status = TaskStatus.WRONG

        if annotation_result.status == TaskStatus.WRONG_NAME and knowledge_level == 2:
            annotation_result.status = TaskStatus.WRONG

        return annotation_result

    @staticmethod
    def __generate_name_feedback(
        *,
        user_annotation: Union[PointResult, LineResult, PolygonResult],
        percentage: float,
        task_feedback: TaskFeedback,
        knowledge_level: int,
    ) -> bool:
        if user_annotation.name_matches:
            TaskResultFactory.append_result_detail(
                annotation_id=user_annotation.id,
                status=TaskStatus.CORRECT,
                percentage=percentage,
                task_result=task_feedback,
            )
            return True
        else:
            if knowledge_level != 2:
                TaskResultFactory.append_result_detail(
                    annotation_id=user_annotation.id,
                    status=TaskStatus.WRONG_NAME,
                    percentage=percentage,
                    task_result=task_feedback,
                )
            else:
                TaskResultFactory.append_result_detail(
                    annotation_id=user_annotation.id,
                    status=TaskStatus.WRONG,
                    percentage=percentage,
                    task_result=task_feedback,
                )
        return False

    @staticmethod
    def generate_image_select_feedback(
        *,
        task_feedback: TaskFeedback,
        correct_image_indices: List[str],
        wrong_image_indices: List[str],
    ) -> TaskFeedback:
        for correct_index in correct_image_indices:
            select_image_feedback = SelectImageFeedback()
            select_image_feedback.status = TaskStatus.CORRECT
            select_image_feedback.image = correct_index
            task_feedback.result_detail.append(select_image_feedback)
        if len(wrong_image_indices) == 0 and len(correct_image_indices) != 0:
            if not task_feedback.task_status:
                TaskResultFactory.correct_status(task_feedback)

        else:
            for wrong_index in wrong_image_indices:
                select_image_feedback = SelectImageFeedback()
                select_image_feedback.status = TaskStatus.WRONG
                select_image_feedback.image = wrong_index
                task_feedback.result_detail.append(select_image_feedback)

            if not task_feedback.task_status:
                task_feedback.task_status = TaskStatus.WRONG
                task_feedback.response_text = (
                    "Du hast noch nicht die richtigen Bilder ausgewählt"
                )

        return task_feedback

    @staticmethod
    def __check_name(
        matched_ids: Dict[str, List[Union[PointResult, LineResult, PolygonResult]]],
        task_result: TaskFeedback,
    ) -> Dict[str, List[Union[PointResult, LineResult, PolygonResult]]]:
        """
        Checks if name is correct

        :param matched_ids:
        :param task_result:
        :return:
        """
        temp = matched_ids
        for key in matched_ids:
            for annotation in matched_ids[key]:
                if "name_matches" in annotation:
                    if not annotation.name_matches:
                        task_result.result_detail.append(
                            AnnotationFeedback(
                                id=annotation.id, status=TaskStatus.WRONG_NAME
                            )
                        )
                        temp[key].remove(annotation)
                else:
                    temp[key].remove(annotation)
        return temp

    @staticmethod
    def __get_best_match_duplicate_hit(
        matched_ids: Dict[str, List[Union[PointResult, LineResult, PolygonResult]]],
        *,
        key: str,
    ) -> Dict[str, List[Union[PointResult, LineResult, PolygonResult]]]:
        result_matched_ids = {}

        solution_ids_to_user_solution = {}
        matched_ids.keys()

        for solution_id in matched_ids:
            for annotation in matched_ids[solution_id]:
                if not annotation.id in solution_ids_to_user_solution:
                    solution_ids_to_user_solution[annotation.id] = [
                        (solution_id, annotation)
                    ]
                else:
                    solution_ids_to_user_solution[annotation.id].append(
                        (solution_id, annotation)
                    )

        for user_solution_id in solution_ids_to_user_solution:
            solution_id = solution_ids_to_user_solution[user_solution_id][0][0]
            annotation = solution_ids_to_user_solution[user_solution_id][0][1]

            best_annotation = annotation
            if len(solution_ids_to_user_solution[user_solution_id]) > 1:
                sorted_best_key = sorted(
                    solution_ids_to_user_solution[user_solution_id],
                    key=lambda x: x[1].dict()[key],
                    reverse=False,
                )
                solution_id = sorted_best_key[0][0]
                best_annotation = sorted_best_key[0][1]
            if solution_id in result_matched_ids:
                result_matched_ids[solution_id].append(best_annotation)
            else:
                result_matched_ids[solution_id] = [best_annotation]

        return result_matched_ids

    @staticmethod
    def __filter_best_match(
        matched_ids: Dict[str, List[Union[PointResult, LineResult, PolygonResult]]],
        *,
        key: str,
    ) -> Dict[str, List[Union[PointResult, LineResult, PolygonResult]]]:
        """
        Filters the annotation matches for the best match

        :param matched_ids: All matched Annotations
        :param key: The key for determining the best match
        :return: The filtered annotation matches
        """
        for solution_id in matched_ids:
            for idx, item in enumerate(matched_ids[solution_id]):
                duplicate_items = FeedbackGenerator.__has_different_hit(
                    matched_ids, solution_id, item.id
                )
                if len(duplicate_items) > 0:
                    if len(matched_ids[solution_id]) > 1:
                        matched_ids[solution_id].remove(item)
                    else:
                        for sol_oid, duplicate_item in duplicate_items:
                            if item.dict()[key] > duplicate_item.dict()[key]:
                                matched_ids[solution_id].remove(item)

        return matched_ids

    @staticmethod
    def __generate_no_match_feedback(
        task_result: TaskFeedback, no_match_ids: List[str]
    ) -> List[AnnotationFeedback]:
        """
        Generates the task feedback for annotations with no match

        :param task_result: The task result object
        :param no_match_ids: The ids with no match
        :return: The generated detail results
        """
        detail_results = []
        for no__match_id in no_match_ids:
            TaskResultFactory.append_result_detail(
                annotation_id=no__match_id,
                status=TaskStatus.WRONG,
                percentage=0.0,
                task_result=task_result,
            )
        return detail_results

    @staticmethod
    def __generate_invalid_feedback(
        task_result: TaskFeedback, invalid_ids: List[str]
    ) -> List[AnnotationFeedback]:
        """
        Generates the task feedback for annotations which are invalid

        :param task_result: The task result object
        :param invalid_ids: The IDs of the annotations which are invalid
        :return: The generated detail results
        """
        detail_results = []
        for no__match_id in invalid_ids:
            TaskResultFactory.append_result_detail(
                annotation_id=no__match_id,
                status=TaskStatus.INVALID,
                percentage=0.0,
                task_result=task_result,
            )
        return detail_results

    @staticmethod
    def __has_different_hit(
        matched_ids: Dict[str, List[Union[PointResult, LineResult, PolygonResult]]],
        solution_id: str,
        result_id: str,
    ) -> List[
        Tuple[Union[str, None], Union[PointResult, LineResult, PolygonResult, None]]
    ]:
        """
        Returns all solution annotations ids and the Result items that are also contained in different solution results

        :param matched_ids: All matched Annotations
        :param solution_id: Id of the solution
        :param result_id: Id of the result item
        :return: The found solutions and results
        """
        duplicate_items = []
        for sol_id in matched_ids:
            if sol_id != solution_id:
                for item in matched_ids[sol_id]:
                    if item.id == result_id:
                        duplicate_items.append((sol_id, item))
        return duplicate_items
