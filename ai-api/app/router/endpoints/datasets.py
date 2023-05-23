from fastapi import APIRouter, Depends
from supertokens_python.recipe import session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
import app.clearml_wrapper.clearml_wrapper as clearml_wrapper

router = APIRouter()


@router.get("")
async def login(s: SessionContainer = Depends(verify_session())):
    return clearml_wrapper.get_datasets()


@router.get("/{dataset_project_id}")
async def get_specific_dataset(
    dataset_project_id: str, s: SessionContainer = Depends(verify_session())
):
    return clearml_wrapper.get_specific_dataset(dataset_project_id)


@router.get("/{dataset_id}/images")
async def get_dataset_images(
    dataset_id: str, _: SessionContainer = Depends(verify_session())
):
    return clearml_wrapper.get_datatset_debug_images(dataset_id)
