from fastapi import APIRouter, Depends
from supertokens_python.recipe import session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
import app.clearml_wrapper.clearml_wrapper as clearml_wrapper

router = APIRouter()


@router.post("")
async def create_project(
    create_body: dict, s: SessionContainer = Depends(verify_session())
):
    project = clearml_wrapper.create_project(
        project_name=create_body["project_name"],
        description=create_body["description"]
        if "description" in create_body
        else None,
    )
    return project


@router.get("")
async def get_projects(s: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_projects()


@router.get("/{project_id}")
async def get_project(project_id: str, _: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_project(project_id)


@router.delete("/{project_id}")
async def delete_project(
    project_id: str, _: SessionContainer = Depends(verify_session())
):
    return clearml_wrapper.delete_project(project_id)


@router.get("/{project_id}/tasks")
async def get_project_tasks(
    project_id: str, s: SessionContainer = Depends(verify_session())
):
    return clearml_wrapper.get_tasks_to_project(project_id)
