import os

from celery import Celery

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
