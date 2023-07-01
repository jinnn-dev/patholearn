from datetime import datetime
from typing import Annotated, List, Optional
from app.crud.dataset import (
    get_dataset,
    get_datasets,
    update_dataset_status,
    delete_dataset,
)

from pydantic import parse_obj_as

from app.database.minio_wrapper import minio_wrapper
from app.schema.dataset import DatasetStatus, DatasetType
from fastapi import APIRouter, Depends, Form, UploadFile, BackgroundTasks
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
import app.clearml_wrapper.clearml_wrapper as clearml_wrapper
from app.utils.logger import logger
import shutil
from uuid import uuid4
import tempfile
import os
from app.schema.dataset import Dataset
from app.database.database import dataset_collection
from app.core.dataset.create_dataset import create_dataset, create_dataset_backgroud
from clearml import Dataset as ClearmlDataset

router = APIRouter()


@router.post("")
async def create_new_dataset(
    background_tasks: BackgroundTasks,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    dataset_type: Annotated[DatasetType, Form()],
    is_grayscale: Annotated[str, Form()],
    file: Annotated[UploadFile, Form()] = UploadFile(...),
    s: SessionContainer = Depends(verify_session()),
):
    user_id = s.get_user_id()

    new_dataset = await dataset_collection.insert_one(
        {
            "creator_id": user_id,
            "name": name,
            "description": description,
            "dataset_type": dataset_type,
            "created_at": datetime.now(),
            "status": "saving",
            "metadata": {"is_grayscale": is_grayscale == "true"},
        }
    )

    dataset = await get_dataset(dataset_id=str(new_dataset.inserted_id))
    await update_dataset_status(dataset_id=dataset.id, status="processing")
    background_tasks.add_task(create_dataset_backgroud, dataset=dataset, file=file.file)
    return dataset


@router.get("", response_model=List[Dataset])
async def datasets(_: SessionContainer = Depends(verify_session())):
    return await get_datasets()


@router.get("/{dataset_id}", response_model=Dataset)
async def dataset(dataset_id: str, _: SessionContainer = Depends(verify_session())):
    return await get_dataset(dataset_id)


@router.delete("/{dataset_id}", response_model=Dataset)
async def dataset_delete(
    dataset_id: str, _: SessionContainer = Depends(verify_session())
):
    dataset = await get_dataset(dataset_id)
    if dataset.clearml_dataset is not None:
        clearml_id = dataset.clearml_dataset["id"]
        clearml_project_id = dataset.clearml_dataset["project"]["id"]
        try:
            clearml_dataset = ClearmlDataset.delete(
                clearml_id,
                delete_files=True,
                delete_external_files=True,
                force=True,
                entire_dataset=True,
            )
            clearml_wrapper.delete_project(clearml_project_id)
        except Exception as error:
            logger.exception(
                f"Failed deleting dataset {dataset_id} (ClearML {clearml_id}): {error}"
            )

    await delete_dataset(dataset_id)

    return dataset


# @router.get("")
# async def login(s: SessionContainer = Depends(verify_session())):
#     return clearml_wrapper.get_datasets()


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
