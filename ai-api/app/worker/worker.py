import os
from app.schema.dataset import DatasetDimension

from celery import Celery
from celery.utils.log import get_task_logger
from clearml import Dataset as ClearmlDataset

from app.core.dataset.create_dataset import parse_extracted_folder
from app.clearml_wrapper.clearml_wrapper import (
    add_files_to_dataset,
    create_dataset as create_clearml_dataset,
    finalize_dataset,
    get_dataset_task,
    set_metadata_of_dataset,
)
from app.utils.io import delete_osx_files, unpack_archive, delete_folder
from app.worker.database import get_dataset, update_dataset, update_dataset_status

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "amqp://guest:guest@rabbit:5673//"
)

logger = get_task_logger(__name__)


@celery_app.task(name="create_dataset", queue="ai_api")
def create_dataset(file_path: str, dataset_id: str):
    dataset = get_dataset(dataset_id)
    log_prefix = f"Dataset {dataset_id}: "
    unpack_path = f"/data/{dataset.id}"
    try:
        logger.info(f"{log_prefix} Unpacking archive")
        unpack_archive(file_path, unpack_path)
        delete_osx_files(unpack_path)
    except Exception as error:
        logger.error(f"{log_prefix} Failed unpacking: {error}")
        update_dataset(dataset.id, {"status": "failed"})
        return

    try:
        logger.info(f"{log_prefix} Parsing folder")
        metadata = parse_extracted_folder(unpack_path)
        dataset.metadata.classes = metadata["classes"]
        dataset.metadata.class_map = metadata["class_map"]
        dataset.metadata.dimension = DatasetDimension(
            x=metadata["dimension"]["x"], y=metadata["dimension"]["y"]
        )
        update_dataset(dataset.id, {"metadata": dataset.metadata.dict()})

    except Exception as error:
        logger.error(f"{log_prefix} Failed parsing: {error}")
        update_dataset(dataset.id, {"status": "failed"})
        return

    logger.info(f"{log_prefix} Creating ClearML dataset")

    clearml_dataset: ClearmlDataset = create_clearml_dataset(
        dataset_name=dataset.name,
        dataset_description=dataset.description,
        dataset_project="Datasets",
        dataset_tags=[dataset.dataset_type],
    )

    try:
        logger.info(f"{log_prefix} Adding files to dataset")
        add_files_to_dataset(clearml_dataset, unpack_path)
    except ValueError as error:
        logger.error(f"{log_prefix} Failed adding files: {error}")
        update_dataset_status(dataset.id, "failed")
        return

    set_metadata_of_dataset(clearml_dataset, dataset.metadata.dict())

    try:
        logger.info(f"Dataset {dataset_id}: Finalizing")
        finalize_dataset(clearml_dataset)
    except Exception as error:
        logger.error(f"{log_prefix} Failed finalizing: {error}")
        update_dataset_status(dataset.id, "failed")
        return

    clearml_dataset = get_dataset_task(clearml_dataset)
    update_dataset(dataset_id=dataset.id, fields={"clearml_dataset": clearml_dataset})

    delete_folder(unpack_path)

    update_dataset_status(dataset.id, "completed")
