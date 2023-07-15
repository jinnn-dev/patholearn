from datetime import datetime
import json
import tempfile
from typing import Dict, List, Literal, Optional, Union
from app.train.train_model import start_builder_training
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse, JSONResponse
from pydantic import parse_obj_as
from supertokens_python.recipe import session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from clearml import Task as ClearmlTask
import nbformat as nbf
import app.clearml_wrapper.clearml_wrapper as clearml_wrapper
from app.schema.builder_task import CreateBuilderTask, BuilderTask
from app.database.database import task_collection
from app.schema.task import (
    Graph,
    CreateTask,
    LockElement,
    NodeType,
    Task,
    TaskNoGraph,
    TaskVersion,
    UdateTask,
    UnlockElements,
    UpdateTaskVersion,
)
from app.core.parser.parse_to_pytorch import (
    parse_task_version_to_python,
)
from app.utils.logger import logger
from app.crud.task import get_task_with_version

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


@router.post("/reset", response_model=TaskVersion)
async def reset_version(
    update_data: Dict, _: SessionContainer = Depends(verify_session())
):
    task_id = update_data["task_id"]
    version_id = update_data["version_id"]
    task, version = await get_task_with_version(task_id, version_id)
    if version.clearml_id:
        task: ClearmlTask = ClearmlTask.get_task(task_id=version.clearml_id)
        task.delete(delete_artifacts_and_models=True)
    await task_collection.update_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
        },
        {
            "$set": {"versions.$[version].clearml_id": None},
            "$unset": {"versions.$[version].status": 1},
        },
        array_filters=[{"version.id": ObjectId(version_id)}],
    )
    updated_task, updated_version = await get_task_with_version(
        task_id=task_id, version_id=version_id
    )
    return updated_version


@router.put("", response_model=TaskNoGraph)
async def update_task(
    update_task: UdateTask, _: SessionContainer = Depends(verify_session())
):
    update_dict = update_task.dict(exclude_unset=True)
    update_dict.pop("id", None)

    updated_project = await task_collection.update_one(
        {"_id": ObjectId(update_task.id)}, {"$set": update_dict}
    )
    return await task_collection.find_one(
        {"_id": ObjectId(update_task.id)}, projection={"versions.graph": False}
    )


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


@router.get(
    "/{task_id}",
    response_model=Task,
    description="Returns the Task model to the given id",
)
async def get_task(task_id: str, _: SessionContainer = Depends(verify_session())):
    task = await task_collection.find_one({"_id": ObjectId(task_id)})
    return task


@router.delete(
    "/{task_id}", response_model=int, description="Deletes the task to the given id"
)
async def delete_task(task_id: str, _: SessionContainer = Depends(verify_session())):
    task = await task_collection.delete_one({"_id": ObjectId(task_id)})
    return task.deleted_count


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


@router.post("/{task_id}/version/{version_id}/train")
async def start_task_training(
    task_id: str, version_id: str, _: SessionContainer = Depends(verify_session())
):
    task, task_version = await get_task_with_version(task_id, version_id)

    if task is None or task_version is None:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        (
            pytorch_text,
            _,
            dataset_id,
            dataset_clearml_id,
        ) = await parse_task_version_to_python(task, task_version)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Model could not be parsed")

    await task_collection.update_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
        },
        {"$set": {"versions.$[version].status": "creating"}},
        array_filters=[{"version.id": ObjectId(version_id)}],
    )

    start_builder_training(
        pytorch_text, task_id, task.name, version_id, dataset_clearml_id, dataset_id
    )

    try:
        pytorch_text, _, _, _ = await parse_task_version_to_python(task, task_version)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Model could not be parsed")

    return pytorch_text


@router.get(
    "/{task_id}/version/{version_id}/download",
)
async def download_builder_version(
    task_id: str, version_id: str, language: Literal["python", "jupyter"] = "python"
):
    task, task_version = await get_task_with_version(task_id, version_id)

    if task is None or task_version is None:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        pytorch_text, model, _, _ = await parse_task_version_to_python(
            task, task_version, False
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Model could not be parsed")

    if language == "python":
        return PlainTextResponse(content=pytorch_text, media_type="text/x-python")
    else:
        nb = nbf.v4.new_notebook()

        model_dict = model.dict()
        for key, value in model_dict.items():
            if key == "ignore_clearml" or value is None:
                continue
            cell = nbf.v4.new_code_cell(source=value)
            nb["cells"].append(cell)

        return JSONResponse(json.loads(nbf.writes(nb)))


@router.get("/{task_id}/version/{version_id}/parse")
async def parse_builder_version(
    task_id: str, version_id: str, s: SessionContainer = Depends(verify_session())
):
    task, task_version = await get_task_with_version(task_id, version_id)

    if task is None or task_version is None:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        pytorch_text, _, _, _ = await parse_task_version_to_python(task, task_version)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Model could not be parsed")

    return pytorch_text


@router.get(
    "/{task_id}/version/{version_id}/metrics/latest", response_model=Optional[Dict]
)
async def get_latest_task_metrics(
    task_id: str, version_id: str, _: SessionContainer = Depends(verify_session())
):
    _, version = await get_task_with_version(task_id, version_id)
    parsed_version = parse_obj_as(TaskVersion, version)

    if parsed_version.clearml_id is not None:
        try:
            clearml_task: ClearmlTask = ClearmlTask.get_task(
                task_id=parsed_version.clearml_id
            )
            metrics = clearml_task.get_last_scalar_metrics()
            return metrics
        except Exception as e:
            logger.exception(e)
            return None
    return None


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
