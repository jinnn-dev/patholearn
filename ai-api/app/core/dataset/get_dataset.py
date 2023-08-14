import os

from app.schema.dataset import Dataset
import app.clearml_wrapper.clearml_wrapper as clearml_wrapper


def fetch_dataset_images(dataset: Dataset):
    if dataset.clearml_dataset:
        debug_images = clearml_wrapper.get_datatset_debug_images(
            dataset.clearml_dataset["id"]
        )
        replace_string = os.environ.get("AI_STORAGE_INTERNAL_URL")
        object_storage = os.environ.get("AI_STORAGE_PUBLIC_URL")
        debug_images = [
            image.replace(replace_string, object_storage) for image in debug_images
        ]
        return debug_images
    return None
