import json
import os
import subprocess
from bson import ObjectId

from celery import Celery
from celery.utils.log import get_task_logger
from clearml import Task, Model, Dataset
from pydantic import parse_obj_as
from app.database.database import task_collection
from app.scheduler.session import SessionManager
from app.scheduler.models import IntervalSchedule, PeriodicTask
from app.ws.client import trigger_ws_task_event, trigger_ws_task_status_changed
from app.core.serve import serve_model, remove_model, check_if_model_available

from app.scheduler.modify import remove_periodic_task, create_periodic_task

from app.crud.task_version import (
    update_version_clearml_id,
    update_version_dataset_id,
    update_version_status,
)
from app.core.train import write_training_file, start_training_file

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "amqp://guest:guest@rabbit:5673//"
)
beat_dburi = "sqlite:///app/scheduler/schedule.db"
celery_app.conf.update({"beat_dburi": beat_dburi})

logger = get_task_logger(__name__)

session_manager = SessionManager()
session = session_manager.session_factory(beat_dburi)
session.close()


@celery_app.task(name="enqueue_builder_task", queue="ai")
def enqueue_builder_task(
    file_contents: str,
    task_id: str,
    task_name: str,
    version_id: str,
    dataset_clearml_id: str,
    dataset_id: str,
):
    logger.info(f"Writing python file for {task_id} ({task_name})")
    script_path = write_training_file(file_contents)

    logger.info(f"Starting script for {task_id} ({task_name})")
    stdout, stderr, exit_code = start_training_file(script_path)

    logger.info(f"Script {task_id} stdout: {stdout}")
    logger.error(f"Script {task_id} stderr: {stderr}")
    logger.info(f"Script {task_id} exit code: {exit_code}")
    if exit_code != 0:
        status = "failed"
        update_version_status(task_id, version_id, status)
        trigger_ws_task_status_changed(
            task_id, old_status="creating", new_status=status
        )
        return

    try:
        task: Task = Task.get_task(project_name=task_name, task_name=version_id)
    except Exception as e:
        logger.exception(e)
        update_version_status(task_id, version_id, "failed")
        trigger_ws_task_status_changed(
            task_id, old_status="creating", new_status="failed"
        )
        return

    update_version_clearml_id(task_id, version_id, task.id)
    trigger_ws_task_event(task_id, "training-clearml", task.id)

    update_version_status(task_id, version_id, task.status)
    trigger_ws_task_status_changed(
        task_id, old_status="creating", new_status=task.status
    )

    update_version_dataset_id(task_id, version_id, dataset_id)

    create_periodic_task(
        peridodic_task_name=task.id,
        task_name="check_task_status",
        data={
            "clearml_task_id": task.id,
            "task_id": task_id,
            "version_id": version_id,
            "dataset_id": dataset_clearml_id,
        },
    )

    logger.info(f"Created Periodic task: {task.id}")

    return 0


@celery_app.task(name="check_task_status", queue="ai")
def check_task_version(
    clearml_task_id: str, task_id: str, version_id: str, dataset_id: str
):
    _, session_maker = session_manager.create_session(beat_dburi)
    session = session_maker()
    try:
        clearml_task: Task = Task.get_task(task_id=clearml_task_id)
    except ValueError as error:
        logger.exception(error)
        remove_periodic_task(clearml_task_id, session)
        return

    new_status = clearml_task.status

    if new_status != "completed":
        metrics = clearml_task.get_last_scalar_metrics()
        if metrics is not None and metrics:
            trigger_ws_task_event(task_id, "training-metrics", metrics)
            trigger_ws_task_event(task_id, "training-metrics-diagram", True)

        trigger_ws_task_event(task_id, "training-logs", True)

    if new_status == "failed":
        remove_periodic_task(clearml_task.id, session)

    db_task = task_collection.find_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
        },
    )
    old_status = db_task["versions"][0]["status"]

    if old_status != new_status:
        trigger_ws_task_status_changed(
            task_id, old_status=old_status, new_status=new_status
        )
        update_version_status(task_id, version_id, new_status)

    if new_status == "completed":
        stdout, stderr, exit_code = serve_model(clearml_task, dataset_id)

        logger.info(f"Script Serving {task_id} stdout: {stdout}")
        logger.error(f"Script Serving {task_id} stderr: {stderr}")
        logger.info(f"Script Serving {task_id} exit code: {exit_code}")
        remove_periodic_task(clearml_task.id, session)
        create_periodic_task(
            peridodic_task_name=clearml_task_id,
            task_name="check_serve_endpoint",
            data={
                "task_id": task_id,
                "clearml_task_id": clearml_task.id,
                "dataset_id": dataset_id,
            },
            session=session,
        )

    return 0


@celery_app.task(name="check_serve_endpoint", queue="ai")
def check_serve_endpoint(task_id: str, clearml_task_id: str, dataset_id: str):
    is_available = check_if_model_available(clearml_task_id, dataset_id)
    logger.info(f"Serve is available: {is_available}")
    if is_available:
        trigger_ws_task_event(task_id, "serve-is-available", True)
        remove_periodic_task(clearml_task_id)
    pass


@celery_app.task(name="remove_serve_endpoint", queue="ai")
def remove_model_serve_endpoint(clearml_task_id: str):
    stdout, stderr, exit_code = remove_model(clearml_task_id)

    logger.info(f"Script Serving {clearml_task_id} stdout: {stdout}")
    logger.error(f"Script Serving {clearml_task_id} stderr: {stderr}")
    logger.info(f"Script Serving {clearml_task_id} exit code: {exit_code}")
