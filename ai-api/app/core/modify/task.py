from bson import ObjectId
from pydantic import parse_obj_as
from typing import List

from app.schema.task import Task
from app.database.database import task_collection
from app.core.modify.task_version import remove_clearml_task_to_version


async def remove_task(task_id: str, task: Task = None):
    if task is None:
        db_task = await task_collection.find_one({"_id": ObjectId(task_id)})
        task = parse_obj_as(Task, db_task)
    for version in task.versions:
        if version.clearml_id:
            remove_clearml_task_to_version(version)

    task = await task_collection.delete_one({"_id": ObjectId(task_id)})
    return task.deleted_count


async def remove_tasks(tasks: List[Task]):
    delete_count_sum = 0
    for task in tasks:
        delete_count_sum += await remove_task(task.id, task)
    return delete_count_sum
