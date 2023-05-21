from bson import ObjectId
from fastapi import APIRouter, Body, Depends
from supertokens_python.recipe import session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
import app.clearml_wrapper.clearml_wrapper as clearml_wrapper
from app.schema.builder_task import CreateBuilderTask, BuilderTask
from app.database.database import task_collection

router = APIRouter()


@router.post("/builder", response_model=BuilderTask, status_code=201)
async def create_builder_task(
    data: CreateBuilderTask = Body(...), s: SessionContainer = Depends(verify_session())
):
    user_id = s.get_user_id()
    new_task = await task_collection.insert_one(
        {"name": data.name, "user_id": user_id, "project_id": data.project_id}
    )
    created_task = await task_collection.find_one({"_id": new_task.inserted_id})
    print(created_task)
    return created_task


@router.get("/builder/{task_id}", response_model=BuilderTask)
async def create_builder_task(
    task_id: str, s: SessionContainer = Depends(verify_session())
):
    print(task_id)
    found_task = await task_collection.find_one({"_id": ObjectId(task_id)})
    return found_task


@router.post("")
async def create_task(data: dict, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.create_task_and_enque(data)


@router.get("/{task_id}")
async def get_task(task_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_task(task_id)


@router.get("/{task_id}/log")
async def get_task_log(task_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_task_log(task_id)


@router.get("/{task_id}/metrics")
async def get_task_log(task_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_task_metrics(task_id)