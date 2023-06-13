import os

from celery import Celery
from app.utils.logger import logger

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "amqp://guest:guest@rabbit:5673//"
)


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


def start_builder_training(
    file_contents: str, task_id: str, task_name: str, version_id: str
):
    result = celery_app.send_task(
        name="enqueue_builder_task",
        args=[file_contents, task_id, task_name, version_id],
        retries=3,
        queue="ai",
    )

    logger.info(f"Celery result: {result}")
