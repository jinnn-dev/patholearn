import json
import os
import subprocess
from bson import ObjectId

from celery import Celery
from celery.utils.log import get_task_logger
from clearml import Task
from pydantic import parse_obj_as
from app.database.database import task_collection
from app.scheduler.session import SessionManager
from app.scheduler.models import IntervalSchedule, PeriodicTask
from app.ws.client import ws_client

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


def update_version_status(task_id: str, version_id: str, status: str):
    task_collection.update_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
        },
        {"$set": {"versions.$[version].status": status}},
        array_filters=[{"version.id": ObjectId(version_id)}],
    )


def update_version_clearml_id(task_id: str, version_id: str, clearml_id: str):
    task_collection.update_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
        },
        {"$set": {"versions.$[version].clearml_id": clearml_id}},
        array_filters=[{"version.id": ObjectId(version_id)}],
    )


@celery_app.task(name="enqueue_builder_task", queue="ai")
def enqueue_builder_task(
    file_contents: str, task_id: str, task_name: str, version_id: str
):
    script_path = "/app/builder_train.py"
    file = os.open(
        script_path,
        flags=(
            os.O_RDWR
            | os.O_CREAT  # create if not exists
            | os.O_TRUNC  # truncate the file to zero
        ),
        mode=0o777,
    )

    logger.info(f"Writing python file for {task_id} ({task_name})")
    with open(script_path, "w") as file:
        file.write(file_contents)

    logger.info(f"Starting script for {task_id} ({task_name})")
    command = ["python", script_path]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Read from stdout and stderr
    stdout, stderr = p.communicate()

    exit_code = p.wait()
    # Convert byte stream to string
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")

    logger.info(f"Script {task_id} stdout: {stdout}")
    logger.error(f"Script {task_id} stderr: {stderr}")
    logger.info(f"Script {task_id} exit code: {exit_code}")
    if exit_code != 0:
        status = "failed"
        update_version_status(task_id, version_id, status)
        ws_client.trigger(
            f"presence-task-{task_id}",
            "training-status-changed",
            {"old": "creating", "new": "failed"},
        )
        return

    try:
        task: Task = Task.get_task(project_name=task_name, task_name=version_id)
    except Exception as e:
        update_version_status(task_id, version_id, "failed")
        ws_client.trigger(
            f"presence-task-{task_id}",
            "training-status-changed",
            {"old": "creating", "new": "failed"},
        )
        return

    update_version_clearml_id(task_id, version_id, task.id)
    update_version_status(task_id, version_id, task.status)
    ws_client.trigger(
        f"presence-task-{task_id}",
        "training-status-changed",
        {"old": "creating", "new": task.status},
    )
    ws_client.trigger(
        f"presence-task-{task_id}",
        "training-clearml",
        task.id,
    )
    _, session_maker = session_manager.create_session(beat_dburi)
    session = session_maker()
    schedule = (
        session.query(IntervalSchedule)
        .filter_by(every=1, period=IntervalSchedule.SECONDS)
        .first()
    )
    if not schedule:
        schedule = IntervalSchedule(every=5, period=IntervalSchedule.SECONDS)
        session.add(schedule)
        session.commit()
    logger.info(f"Schedule to use: {schedule}")

    task = PeriodicTask(
        interval=schedule,
        name=task.id,
        task="check_task_status",
        kwargs=json.dumps(
            {
                "clearml_task_id": task.id,
                "task_id": task_id,
                "task_name": task_name,
                "version_id": version_id,
            }
        ),
        queue="ai",
    )
    session.add(task)
    session.commit()

    logger.info(f"Created Periodic task: {task}")

    return 0


@celery_app.task(name="check_task_status", queue="ai")
def check_task_version(
    clearml_task_id: str, task_id: str, task_name: str, version_id: str
):
    _, session_maker = session_manager.create_session(beat_dburi)
    session = session_maker()

    clearml_task: Task = Task.get_task(task_id=clearml_task_id)
    new_status = clearml_task.status

    metrics = clearml_task.get_last_scalar_metrics()
    if metrics is not None and metrics:
        websocket_result = ws_client.trigger(
            f"presence-task-{task_id}",
            "training-metrics",
            metrics,
        )

    if new_status == "completed" or new_status == "failed":
        periodic_task = (
            session.query(PeriodicTask).filter_by(name=clearml_task_id).first()
        )
        if periodic_task is not None:
            session.delete(periodic_task)
            session.commit()

    db_task = task_collection.find_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
        },
    )
    old_status = db_task["versions"][0]["status"]

    if old_status != new_status:
        websocket_result = ws_client.trigger(
            f"presence-task-{task_id}",
            "training-status-changed",
            {"old": old_status, "new": new_status},
        )
        logger.info(f"Websocket result ({task_id}): {websocket_result}")

        task_collection.update_one(
            {
                "_id": ObjectId(task_id),
                "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
            },
            {"$set": {"versions.$[version].status": new_status}},
            array_filters=[{"version.id": ObjectId(version_id)}],
        )

    return 0


@celery_app.task(name="enqueue_task", queue="ai")
def enqueue_task(project_name, task_name, dataset_id, model_name):
    script_name = "/app/train.py"
    arguments = [
        "--dataset_id",
        dataset_id,
        "--model_name",
        model_name,
        "--project_name",
        project_name,
        "--task_name",
        task_name,
    ]
    # cmd = f"python /app/train.py --dataset_id {dataset_id} --model_name {model_name} --projet_name {project_name} -task_name {task_name}"
    command = ["python", script_name] + arguments
    # cmd = "ls -la /app"
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p = subprocess.Popen(command)
    exit_code = p.wait()
    logger.info(exit_code)
    # out, err = p.communicate()
    # result = str(out).split("\n")
    # for lin in result:
    #     if not lin.startswith("#"):
    #         print(lin)
    # print("Out", out)
    # print("Err", err)
    # main(project_name, task_name, dataset_id, model_name)
    # task: Task = Task.create(
    #     project_name=project_name,
    #     task_name=task_name,
    #     script="/train.py",
    #     argparse_args=[
    #         ("dataset_id", dataset_id),
    #         ("model_name", model_name),
    #         ("project_name", project_name),
    #         ("task_name", task_name),
    #     ],
    #     requirements_file="/clearml.requirements.txt",
    #     add_task_init_call=True,
    # )
    # # Task.enqueue(task, queue_name="default")
