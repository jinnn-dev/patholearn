from clearml import Task
from app.schema.task import TaskVersion
from app.core.serve.modify import remove_serve_endpoint
from app.utils.logger import logger


def remove_clearml_task_to_version(version: TaskVersion):
    if version.clearml_id:
        try:
            task: Task = Task.get_task(task_id=version.clearml_id)
            task.delete(
                delete_artifacts_and_models=True, skip_models_used_by_other_tasks=False
            )
            remove_serve_endpoint(task.id)
        except Exception as e:
            logger.exception(e)
