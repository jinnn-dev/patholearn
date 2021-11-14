import base64
import os
from typing import Any, List, Dict

import aiofiles
from fastapi import UploadFile, File

from app.schemas.slide import Slide
from app.worker import convert_slide


def convert_binary_to_base64(binary_data: bytes):
    """
    Converts bytes to base64

    :param binary_data: Data to convert
    :return: The data in base64
    """
    return base64.b64encode(binary_data)


def is_byte_data(data: Any):
    """
    Checks if the given data is of type byte

    :param data: The data to check
    :return: Whether the data is of type bytes or not
    """
    return type(data) is bytes


def convert_binary_metadata_to_base64(slides: List[Slide]) -> List[Slide]:
    """
    Converts all binary data contained in the slide metadata to base64

    :param slides: The slides to convert the metadata from
    :return: The slides without binary metadata
    """
    for slide in slides:
        if slide.metadata is not None:
            for metadata_key, metadata_value in slide.metadata.items():
                if is_byte_data(metadata_value):
                    slide.metadata[metadata_key] = convert_binary_to_base64(metadata_value)
    return slides


async def write_file(folder_name: str, file_name: str, file: UploadFile = File(...)) -> None:
    """
    Writes the given file asynchronously in a chunkwise manner to the disk.
    File must be stored in a separate folder.
    All data written will be stored in the data folder

    :param folder_name: The name of the folder to store the file in
    :param file_name: The name of the file
    :param file: The file to save on the disk
    :return: The coroutine which can be awaited
    """
    async with aiofiles.open(f"/data/{folder_name}/{file_name}", "wb") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)


async def write_slide_to_disk(folder_name: str, file_name: str, file: UploadFile = File(...)) -> None:
    """
    Creates a image pyramid from the given file.
    All images are stored in the given folder name

    :param folder_name: The name of the folder where to store the slide
    :param file_name: The name of the file
    :param file: The file to save an create a slide from
    """
    os.mkdir(f"/data/{folder_name}")
    await write_file(folder_name, file_name, file)
    convert_slide.delay(file_name)


def remove_truth_values_from_dict(dict_to_be_filtered: Dict[Any, Any]) -> Dict[Any, Any]:
    query = {}
    if dict_to_be_filtered:
        for key in dict_to_be_filtered:
            if not dict_to_be_filtered[key]:
                query[key] = dict_to_be_filtered[key]

    return query
