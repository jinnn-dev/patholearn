from app.utils.logger import logger
from app.worker.celery import celery_app


def start_training(data: dict):
    result = celery_app.send_task(
        name="enqueue_task",
        args=[
            data["project_name"],
            data["task_name"],
            data["dataset_id"],
            data["model_name"],
        ],
        retries=3,
        queue="ai",
    )
    print("Result", result)


def start_task_training(
    file_contents: str,
    task_id: str,
    task_name: str,
    version_id: str,
    clearml_dataset_id: str,
    dataset_id: str,
):
    result = celery_app.send_task(
        name="enqueue_builder_task",
        args=[
            file_contents,
            task_id,
            task_name,
            version_id,
            clearml_dataset_id,
            dataset_id,
        ],
        retries=3,
        queue="ai",
    )

    logger.info(f"Celery result: {result}")
