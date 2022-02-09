import os

import aiofiles
from app.worker import convert_slide
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File


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
