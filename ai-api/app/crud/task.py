from typing import Tuple
from bson import ObjectId
from pydantic import parse_obj_as

from app.database.database import task_collection
from app.schema.task import Task, TaskVersion, TaskNoGraph


async def get_task_with_version(
    task_id: str, version_id: str
) -> Tuple[Task, TaskVersion]:
    db_task = await task_collection.find_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
        },
    )
    if db_task is None:
        return None, None
    task = parse_obj_as(Task, db_task)
    return task, task.versions[0]


async def get_tasks_to_project(project_id: str):
    tasks_cursor = task_collection.find(
        {"project_id": project_id}, projection={"versions.graph": False}
    )
    tasks = []
    async for task in tasks_cursor:
        tasks.append(parse_obj_as(TaskNoGraph, task))
    return tasks
