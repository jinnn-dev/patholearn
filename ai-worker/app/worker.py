import os
import subprocess

from celery import Celery
from celery.utils.log import get_task_logger
from clearml import Task
from app.train import main

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "amqp://guest:guest@rabbit:5673//"
)

logger = get_task_logger(__name__)


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
