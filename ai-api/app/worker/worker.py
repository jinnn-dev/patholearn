import os
import requests
import shutil
import uuid
import cv2
import numpy as np
from patchify import patchify

from app.schema.dataset import DatasetDimension

from celery import Celery
from celery.utils.log import get_task_logger
from clearml import Dataset as ClearmlDataset

from app.core.dataset.create_dataset import (
    parse_extracted_folder,
    parse_segmentation_folder,
)
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


@celery_app.task(name="create_own_dataset", queue="ai_api")
def create_dataset_own(data: dict, dataset_id: str, cookies: dict):
    dataset = get_dataset(dataset_id)
    log_prefix = f"Dataset {dataset_id}: "
    dataset_folder = f"/data/{dataset_id}/"
    os.makedirs(dataset_folder, exist_ok=True)

    downloaded_slides = []
    mask_paths = []
    image_paths = []
    task_ids = []
    annotation_groups = []
    for selected_task in data["tasks"]:
        task_id = selected_task["task"]["id"]
        task_ids.append(task_id)
        url = f"""http://{os.environ.get('LEARN_API_HOST', 'learn_api')}:{os.environ.get('LEARN_API_PORT', '8000')}/tasks/task/{task_id}/mask"""
        response = requests.get(url, cookies=cookies, stream=True)
        mask_path = f"{dataset_folder}/{str(task_id)}.png"
        mask_paths.append(mask_path)

        with open(mask_path, "wb") as out_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    out_file.write(chunk)

        slide_id = selected_task["baseTask"]["slide_id"]
        logger.info(slide_id)
        if slide_id not in downloaded_slides:
            slide_url = f"""http://{os.environ.get('SLIDE_API_HOST', 'slide_api')}:{os.environ.get('SLIDE_API_PORT', '8000')}/slides/{slide_id}/download/-1"""
            response = requests.get(slide_url, cookies=cookies, stream=True)
            downloaded_slides.append(slide_id)
            image_path = f"{dataset_folder}/{str(slide_id)}.png"
            image_paths.append(image_path)
            with open(image_path, "wb") as out_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        out_file.write(chunk)

    image_output_folder = f"{dataset_folder}/images/"
    mask_output_folder = f"{dataset_folder}/masks/"

    os.makedirs(image_output_folder, exist_ok=True)
    os.makedirs(mask_output_folder, exist_ok=True)

    rescale = data["patchMagnification"]
    patch_size = data["patchSize"]
    stride = patch_size
    all_image_patches = []

    for path in image_paths:
        image = cv2.imread(path, cv2.COLOR_BGR2RGB)
        logger.info(image.shape)
        image = rescale_image(image, rescale)
        image_patches = patchify(image, (patch_size, patch_size, 3), step=stride)
        all_image_patches.append(image_patches)
        os.remove(path)
    logger.info("Mask")
    all_mask_patches = []
    for mask_path in mask_paths:
        im_gray = cv2.imread(mask_path)
        logger.info(im_gray.shape)
        resized = rescale_image(im_gray, rescale, interpolate=False)
        result_mask = np.asarray(resized)
        mask_patches = patchify(result_mask, (patch_size, patch_size, 3), step=stride)
        all_mask_patches.append(mask_patches)
        os.remove(mask_path)

    for index, (image_patches, mask_patches) in enumerate(
        zip(all_image_patches, all_mask_patches)
    ):
        for i in range(mask_patches.shape[0]):
            for j in range(mask_patches.shape[1]):
                single_patch_mask = mask_patches[i, j, 0, :, :]

                # # Check if the mask patch only contains the background (0, 0, 0)
                # if np.all(single_patch_mask == [0, 0, 0]):
                #     continue  # If true, skip this iteration and don't save the image or mask patch

                # Save the corresponding image patch if the mask patch is valid
                single_patch_img = image_patches[i, j, 0, :, :]

                image_shape = single_patch_img.shape
                mask_shape = single_patch_mask.shape
                logger.info(f"Image: {image_shape}")
                logger.info(f"Mask: {mask_shape}")
                if image_shape[0] != image_shape[1] or mask_shape[0] != mask_shape[1]:
                    continue
                cv2.imwrite(
                    image_output_folder
                    + str(index)
                    + "_"
                    + str(i)
                    + "_"
                    + str(j)
                    + ".png",
                    single_patch_img,
                )

                # Save the mask patch
                cv2.imwrite(
                    mask_output_folder
                    + str(index)
                    + "_"
                    + str(i)
                    + "_"
                    + str(j)
                    + ".png",
                    single_patch_mask,
                )
    try:
        groups = {}
        for internal_task_id in task_ids:
            annotation_groups_url = f"http://{os.environ.get('LEARN_API_HOST', 'slide_api')}:{os.environ.get('LEARN_API_PORT', '8000')}/tasks/task/{internal_task_id}/annotationGroup"
            response = requests.get(annotation_groups_url, cookies=cookies)
            annotation_groups.append(response.json())
        # [{"name":"invasive tumor","color":"#FF00FF"},{"name":"intraepithelial neoplasia","color":"#ff9600"},{"name":"extralobular duct","color":"#0000ff"},{"name":"lobule (including intralobular ducts)","color":"#00ffff"},{"name":"necrosis","color":"#646400"}]
        groups["background"] = {"index": 0, "color": [0, 0, 0]}
        current_index = 1
        for annotation_group in annotation_groups:
            for group in annotation_group:
                logger.info(group)
                color = tuple(
                    int(group["color"].lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)
                )
                name = group["name"]
                if name not in groups:
                    groups[name] = {"index": current_index, "color": color}
                    current_index += 1
        logger.info(f"{log_prefix} Groups: {groups}")
        logger.info(f"{log_prefix} Parsing folder")
        dataset.metadata.class_map = groups
        dataset.metadata.dimension = DatasetDimension(x=patch_size, y=patch_size)
        dataset.metadata.patch_size = patch_size
        dataset.metadata.patch_magnification = rescale
        dataset.metadata.task_ids = task_ids
        dataset.metadata.dataset_type = dataset.dataset_type
        update_dataset(dataset.id, {"metadata": dataset.metadata.dict()})
    except Exception as error:
        logger.exception(f"{log_prefix} Failed parsing: {error}")
        update_dataset(dataset.id, {"status": "failed"})
        return
    clearml_dataset: ClearmlDataset = create_clearml_dataset(
        dataset_name=dataset.name,
        dataset_description=dataset.description,
        dataset_project="Datasets",
        dataset_tags=[dataset.dataset_type],
    )

    try:
        logger.info(f"{log_prefix} Adding files to dataset")
        add_files_to_dataset(clearml_dataset, dataset_folder)
    except ValueError as error:
        logger.exception(f"{log_prefix} Failed adding files: {error}")
        update_dataset_status(dataset.id, "failed")
        return

    set_metadata_of_dataset(clearml_dataset, dataset.metadata.dict())
    try:
        logger.info(f"Dataset {dataset_id}: Finalizing")
        finalize_dataset(clearml_dataset)
    except Exception as error:
        logger.exception(f"{log_prefix} Failed finalizing: {error}")
        update_dataset_status(dataset.id, "failed")
        return

    clearml_dataset = get_dataset_task(clearml_dataset)
    update_dataset(dataset_id=dataset.id, fields={"clearml_dataset": clearml_dataset})

    delete_folder(dataset_folder)
    update_dataset_status(dataset.id, "completed")


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
        logger.exception(f"{log_prefix} Failed unpacking: {error}")
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
        dataset.metadata.is_grayscale = metadata["is_grayscale"]
        dataset.metadata.dataset_type = dataset.dataset_type
        update_dataset(dataset.id, {"metadata": dataset.metadata.dict()})

    except Exception as error:
        logger.exception(f"{log_prefix} Failed parsing: {error}")
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
        logger.exception(f"{log_prefix} Failed adding files: {error}")
        update_dataset_status(dataset.id, "failed")
        return

    set_metadata_of_dataset(clearml_dataset, dataset.metadata.dict())

    try:
        logger.info(f"Dataset {dataset_id}: Finalizing")
        finalize_dataset(clearml_dataset)
    except Exception as error:
        logger.exception(f"{log_prefix} Failed finalizing: {error}")
        update_dataset_status(dataset.id, "failed")
        return

    clearml_dataset = get_dataset_task(clearml_dataset)
    update_dataset(dataset_id=dataset.id, fields={"clearml_dataset": clearml_dataset})

    delete_folder(unpack_path)
    update_dataset_status(dataset.id, "completed")


@celery_app.task(name="create_segmentation_dataset", queue="ai_api")
def create_segmentation_dataset(file_path: str, dataset_id: str):
    dataset = get_dataset(dataset_id)
    log_prefix = f"Dataset {dataset_id}: "
    unpack_path = f"/data/{dataset.id}"
    try:
        logger.info(f"{log_prefix} Unpacking archive")
        unpack_archive(file_path, unpack_path)
        delete_osx_files(unpack_path)
    except Exception as error:
        logger.exception(f"{log_prefix} Failed unpacking: {error}")
        update_dataset(dataset.id, {"status": "failed"})
        return

    try:
        logger.info(f"{log_prefix} Parsing folder")
        metadata = parse_segmentation_folder(unpack_path)
        dataset.metadata.class_map = metadata["class_map"]
        dataset.metadata.dimension = DatasetDimension(
            x=metadata["dimension"]["x"], y=metadata["dimension"]["y"]
        )
        dataset.metadata.dataset_type = dataset.dataset_type
        update_dataset(dataset.id, {"metadata": dataset.metadata.dict()})

    except Exception as error:
        logger.exception(f"{log_prefix} Failed parsing: {error}")
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
        logger.exception(f"{log_prefix} Failed adding files: {error}")
        update_dataset_status(dataset.id, "failed")
        return

    set_metadata_of_dataset(clearml_dataset, dataset.metadata.dict())

    try:
        logger.info(f"Dataset {dataset_id}: Finalizing")
        finalize_dataset(clearml_dataset)
    except Exception as error:
        logger.exception(f"{log_prefix} Failed finalizing: {error}")
        update_dataset_status(dataset.id, "failed")
        return

    clearml_dataset = get_dataset_task(clearml_dataset)
    update_dataset(dataset_id=dataset.id, fields={"clearml_dataset": clearml_dataset})

    delete_folder(unpack_path)
    update_dataset_status(dataset.id, "completed")


def rescale_image(image: np.ndarray, rescale: float, interpolate: bool = True):
    width = int(image.shape[1] * rescale)
    height = int(image.shape[0] * rescale)
    dim = (width, height)
    return cv2.resize(
        image, dim, interpolation=cv2.INTER_AREA if interpolate else cv2.INTER_NEAREST
    )
