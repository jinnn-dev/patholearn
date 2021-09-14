from app.schemas.task import TaskFeedback, TaskStatus, AnnotationFeedback


class TaskResultFactory:
    @staticmethod
    def correct_status(task_result: TaskFeedback) -> TaskFeedback:
        """
        Returns TaskResult with correct status

        :param task_result: TaskResult object
        :return: The TaskResult with correct status
        """
        task_result.task_status = TaskStatus.CORRECT
        task_result.response_text = "Richtig gelöst!"
        return task_result

    @staticmethod
    def partial_status(task_result: TaskFeedback) -> TaskFeedback:
        """
        Returns TaskResult with partial status

        :param task_result: TaskResult object
        :return: The TaskResult with partial status
        """
        task_result.task_status = TaskStatus.PARTIAL
        task_result.response_text = "Einige Annotationen sind noch nicht richtig!"
        return task_result

    @staticmethod
    def wrong_status(task_result: TaskFeedback) -> TaskFeedback:
        """
        Return TaskResult with wrong status

        :param task_result: TaskResult object
        :return: The TaskResult with wrong status
        """
        task_result.task_status = TaskStatus.WRONG
        task_result.response_text = "Deine Annotationen sind nicht an der richtigen Stelle."
        return task_result

    @staticmethod
    def wrong_name_status(task_result: TaskFeedback) -> TaskFeedback:
        """
        Return TaskResult with wrong_name status

        :param task_result: TaskResult object
        :return: The TaskResult with wrong_name status
        """
        task_result.task_status = TaskStatus.WRONG_NAME
        task_result.response_text = "Deine Annotationen sind an der richtigen Stelle, aber bei den Klassennanmen musst du nochmal schauen"
        return task_result

    @staticmethod
    def append_result_detail(*, annotation_id: str, status: TaskStatus, percentage: float,
                             task_result: TaskFeedback) -> TaskFeedback:
        """
        Appends a new TaskResultDetail to the given TaskResult

        :param annotation_id: Id of the annotation
        :param status: Status of the annotation
        :param percentage: Percentage of the annotation
        :param task_result: TaskResult where the TaskResultDetail should be added to
        :return: The TaskResult with the added TaskResultDetail
        """
        task_result.result_detail.append(AnnotationFeedback(id=annotation_id, status=status, percentage=percentage))
        return task_result

