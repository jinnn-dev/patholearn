from bson import ObjectId
from pydantic import parse_obj_as

from app.schema.task import Task
from app.database.database import task_collection
from app.core.modify.task_version import remove_clearml_task_to_version


async def remove_task(task_id: str):
    db_task = await task_collection.find_one({"_id": ObjectId(task_id)})
    task = parse_obj_as(Task, db_task)
    for version in task.versions:
        if version.clearml_id:
            remove_clearml_task_to_version(version)

    task = await task_collection.delete_one({"_id": ObjectId(task_id)})
    return task.deleted_count
