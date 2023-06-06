import os
import subprocess
from bson import ObjectId

from celery import Celery
from celery.utils.log import get_task_logger
from clearml import Task
from app.train import main
from app.database.database import task_collection

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "amqp://guest:guest@rabbit:5673//"
)

logger = get_task_logger(__name__)


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
    with open(script_path, "w") as file:
        file.write(file_contents)

    command = ["python", script_path]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Read from stdout and stderr
    stdout, stderr = p.communicate()

    exit_code = p.wait()
    # Convert byte stream to string
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")

    print("Standard Output:", stdout)
    print("Standard Error:", stderr)
    print("Exit code:", exit_code)
    status = "CREATED"
    if exit_code != 0:
        status = "FAILED"
        update_version_status(task_id, version_id, status)
        return
    update_version_status(task_id, version_id, status)

    task = Task.get_task(project_name=task_name, task_name=version_id)

    update_version_clearml_id(task_id, version_id, task.id)

    return exit_code


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
