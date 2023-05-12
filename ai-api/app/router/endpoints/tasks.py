from fastapi import APIRouter, Depends
from supertokens_python.recipe import session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
import app.clearml_wrapper.clearml_wrapper as clearml_wrapper

router = APIRouter()


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
