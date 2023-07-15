from app.worker.celery import celery_app


def remove_serve_endpoint(clearml_task_id: str):
    celery_app.send_task(
        name="remove_serve_endpoint", args=[clearml_task_id], retries=3, queue="ai"
    )
