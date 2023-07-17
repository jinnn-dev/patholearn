import datetime
from typing import List

from bson import ObjectId
from pydantic import parse_obj_as
from app.schema.project import (
    CreateProject,
    Project,
    ProjectWithoutTasks,
    UpdateProject,
)
from fastapi import APIRouter, Depends, HTTPException
from supertokens_python.recipe import session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

import app.clearml_wrapper.clearml_wrapper as clearml_wrapper
from app.database.database import task_collection
from app.schema.task import Task, TaskNoGraph
from app.database.database import project_collection
from app.utils.logger import logger
from app.crud.task import get_tasks_to_project
from app.core.modify.task import remove_tasks

router = APIRouter()


@router.post("", response_model=Project)
async def create_project(
    create_project: CreateProject, s: SessionContainer = Depends(verify_session())
):
    new_project = await project_collection.insert_one(
        {
            "name": create_project.name,
            "description": create_project.description,
            "created_at": datetime.datetime.now(),
        }
    )

    created_project = await project_collection.find_one(
        {"_id": new_project.inserted_id}
    )

    logger.debug(created_project)

    return created_project


@router.put("", response_model=Project)
async def update_project(
    update_project: UpdateProject, _: SessionContainer = Depends(verify_session())
):
    update_dict = update_project.dict(exclude_unset=True)
    update_dict.pop("id", None)

    updated_project = await project_collection.update_one(
        {"_id": ObjectId(update_project.id)}, {"$set": update_dict}
    )
    if updated_project.modified_count:
        return await project_collection.find_one({"_id": ObjectId(update_project.id)})
    else:
        raise HTTPException(status_code=404, detail="Project not found")


@router.get("", response_model=List[Project])
async def get_projects(s: SessionContainer = Depends(verify_session())):
    result = []
    async for element in project_collection.find().sort("created_at", -1):
        result.append(element)

    return result


@router.get("/{project_id}", response_model=ProjectWithoutTasks)
async def get_project(project_id: str, _: SessionContainer = Depends(verify_session())):
    project = await project_collection.find_one({"_id": ObjectId(project_id)})
    # tasks = []
    # async for task in task_collection.find({"project_id": project_id}).sort(
    #     "creation_date", -1
    # ):
    #     tasks.append(parse_obj_as(TaskNoGraph, task))

    result = ProjectWithoutTasks(
        project=project,
    )

    return result


@router.delete("/{project_id}")
async def delete_project(
    project_id: str, _: SessionContainer = Depends(verify_session())
):
    db_project = await project_collection.find_one({"_id": ObjectId(project_id)})
    if db_project is None:
        return 0

    tasks = await get_tasks_to_project(project_id)
    await remove_tasks(tasks)
    project_delete_result = await project_collection.delete_one(
        {"_id": ObjectId(project_id)}
    )
    return project_delete_result.deleted_count


@router.post("/clearml")
async def create_clearml_project(
    create_body: dict, s: SessionContainer = Depends(verify_session())
):
    project = clearml_wrapper.create_project(
        project_name=create_body["project_name"],
        description=create_body["description"]
        if "description" in create_body
        else None,
    )
    return project


@router.get("/clearml")
async def get_projects_clearml(s: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_projects()


@router.get("/clearml/{project_id}")
async def get_project(project_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_project(project_id)


@router.delete("/clearml/{project_id}")
async def delete_project_clearml(
    project_id: str, _: SessionContainer = Depends(verify_session())
):
    return clearml_wrapper.delete_project(project_id)


@router.get("/{project_id}/tasks", response_model=List[TaskNoGraph])
async def get_project_tasks(
    project_id: str, _: SessionContainer = Depends(verify_session())
):
    tasks_cursor = task_collection.find(
        {"project_id": project_id}, projection={"versions.graph": False}
    ).sort("creation_date", -1)
    tasks = []
    async for task in tasks_cursor:
        tasks.append(task)
    return tasks


# @router.get("/{project_id}/tasks")
# async def get_project_tasks(
#     project_id: str, s: SessionContainer = Depends(verify_session()
# ):
#     return clearml_wrapper.get_tasks_to_project(project_id)
