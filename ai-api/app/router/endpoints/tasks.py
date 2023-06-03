from datetime import datetime
from typing import List
from bson import ObjectId
from fastapi import APIRouter, Body, Depends
from pydantic import parse_obj_as
from supertokens_python.recipe import session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
import app.clearml_wrapper.clearml_wrapper as clearml_wrapper
from app.schema.builder_task import CreateBuilderTask, BuilderTask
from app.database.database import task_collection
from app.schema.task import (
    Graph,
    CreateTask,
    LockElement,
    Task,
    TaskVersion,
    UnlockElements,
    UpdateTaskVersion,
)
from app.core.parse_graph import parse_graph
from app.core.parse_to_pytorch import parse_to_pytorch_graph
from app.utils.logger import logger

router = APIRouter()


@router.post(
    "",
    response_model=Task,
    description="Creates a new task for building and training a neural network model",
)
async def create_task(
    task_data: CreateTask = Body(...), s: SessionContainer = Depends(verify_session())
):
    user_id = s.get_user_id()
    creation_date = datetime.now()
    new_task = await task_collection.insert_one(
        {
            "creator_id": user_id,
            "project_id": task_data.project_id,
            "name": task_data.name,
            "description": task_data.description,
            "creation_date": creation_date,
            "versions": [
                {
                    "id": ObjectId(),
                    "graph": {"nodes": [], "connections": [], "positions": []},
                    "clearml_id": None,
                    "creation_date": creation_date,
                }
            ],
        }
    )
    created_task = await task_collection.find_one({"_id": new_task.inserted_id})
    return created_task


@router.get(
    "/{task_id}",
    response_model=Task,
    description="Returns the Task model to the given id",
)
async def get_task(task_id: str, _: SessionContainer = Depends(verify_session())):
    task = await task_collection.find_one({"_id": ObjectId(task_id)})
    return task


@router.put(
    "/{task_id}/version",
    description="Updates a version of a Task",
)
async def update_task_version(
    task_id: str,
    update_data: UpdateTaskVersion = Body(...),
    _: SessionContainer = Depends(verify_session()),
):
    # updated_task = await task_collection.update_one(
    #     {
    #         "_id": ObjectId(task_id),
    #         "versions": {"$elemMatch": {"id": ObjectId(update_data.id)}},
    #     },
    #     {"$set": {"versions.$[version].builder"}},
    # )
    update_string = {}
    prefix = "versions.$[version]."
    update_dict = update_data.dict()
    for key in update_dict:
        if key == "id":
            continue
        update_key = prefix + key
        update_string[update_key] = update_dict[key]
    updated_task = await task_collection.update_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(update_data.id)}},
        },
        {"$set": update_string},
        array_filters=[{"version.id": update_data.id}],
        upsert=False,
    )
    return "Ok"


@router.put("/lock")
async def lock_element(
    data: LockElement = Body(...), s: SessionContainer = Depends(verify_session())
):
    # element = await task_collection.find_one(
    #     {
    #         "_id": ObjectId(data.task_id),
    #         "versions": {"$elemMatch": {"id": ObjectId(data.version_id)}},
    #     }
    # )

    element = await task_collection.find_one(
        {
            "_id": ObjectId(data.task_id),
        }
    )

    if element is not None:
        if "lockStatus" not in element or element["lockStatus"] is None:
            set_command = {"$set": {"lockStatus": {data.element_id: data.user_id}}}
        else:
            set_command = {"$set": {f"lockStatus.{data.element_id}": data.user_id}}
        await task_collection.find_one_and_update(
            {
                "_id": ObjectId(data.task_id),
            },
            set_command,
        )

    # element = task_collection.aggregate(
    #     [
    #         {
    #             "$match": {
    #                 "_id": ObjectId(data.task_id),
    #                 "versions.id": ObjectId(data.version_id),
    #                 "versions.graph.nodes.id": data.element_id,
    #             },
    #         }
    #     ]
    # )
    # if element is not None:


@router.put("/unlock")
async def unlock_element(
    data: LockElement = Body(...), s: SessionContainer = Depends(verify_session())
):
    # element = await task_collection.find_one(
    #     {
    #         "_id": ObjectId(data.task_id),
    #         "versions": {"$elemMatch": {"id": ObjectId(data.version_id)}},
    #     }
    # )

    element: Task = await task_collection.find_one(
        {
            "_id": ObjectId(data.task_id),
        }
    )
    if element is not None:
        await task_collection.find_one_and_update(
            {
                "_id": ObjectId(data.task_id),
            },
            {"$unset": {f"lockStatus.{data.element_id}": ""}},
        )


@router.delete("/unlock")
async def unlock_elements(
    data: UnlockElements = Body(...), s: SessionContainer = Depends(verify_session())
):
    # await task_collection.update_many(
    #     {"_id": ObjectId(data.task_id), "lockStatus": data.user_ids},
    #     {"$unset": {f"lockStatus.{data.element_id}": ""}},
    # )

    update_query = {"$unset": {}}
    for key in data.element_ids:
        update_query["$unset"]["lockStatus." + key] = ""
    await task_collection.find_one_and_update(
        {
            "_id": ObjectId(data.task_id),
        },
        update_query,
    )


@router.get("/{task_id}/version/{version_id}/parse")
async def parse_builder_state(
    task_id: str, version_id: str, s: SessionContainer = Depends(verify_session())
):
    task = await task_collection.find_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
        },
    )
    if task is None:
        return
    task_version = parse_obj_as(Graph, task["versions"][0]["graph"])

    parsed_graph = parse_graph(task_version)
    parse_to_pytorch_graph(parsed_graph)


@router.post("/builder", response_model=BuilderTask, status_code=201)
async def create_builder_task(
    data: CreateBuilderTask = Body(...), s: SessionContainer = Depends(verify_session())
):
    user_id = s.get_user_id()
    new_task = await task_collection.insert_one(
        {"name": data.name, "user_id": user_id, "project_id": data.project_id}
    )

    created_task = await task_collection.find_one({"_id": new_task.inserted_id})
    return created_task


@router.get("/builder/{task_id}", response_model=BuilderTask)
async def create_builder_task(
    task_id: str, s: SessionContainer = Depends(verify_session())
):
    print(task_id)
    found_task = await task_collection.find_one({"_id": ObjectId(task_id)})
    return found_task


# @router.post("")
# async def create_task(data: dict, _: SessionContainer = Depends(verify_session())):
#     return clearml_wrapper.create_task_and_enque(data)


# @router.get("/{task_id}")
# async def get_task(task_id: str, _: SessionContainer = Depends(verify_session())):
#     return clearml_wrapper.get_task(task_id)


@router.get("/{task_id}/log")
async def get_task_log(task_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_task_log(task_id)


@router.get("/{task_id}/metrics")
async def get_task_log(task_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_task_metrics(task_id)
