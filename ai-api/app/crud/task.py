from typing import Tuple
from bson import ObjectId
from pydantic import parse_obj_as

from app.database.database import task_collection
from app.schema.task import Task, TaskVersion


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
