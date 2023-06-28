from typing import BinaryIO, Tuple
from uuid import uuid4
import shutil
import os
from app.utils.logger import logger


def write_temporary_file(file: BinaryIO, file_type: str = None) -> Tuple[str, str]:
    """Write the given file to a temporary file on the disc

    Args:
        file: The UploadFile to save on disc

    Returns:
        The path where it saved and the file name
    """
    file_name = uuid4()
    save_path = f"/data/{file_name}" + f".{file_type}" if file_type else ""

    with open(save_path, "wb") as f:
        f.write(file.read())

    return save_path


def unpack_archive(archive_path: str, extract_dir: str):
    shutil.unpack_archive(archive_path, extract_dir)


def delete_osx_files(path: str):
    macosx_dir_path = os.path.join(path, "__MACOSX")
    if os.path.exists(macosx_dir_path) and os.path.isdir(macosx_dir_path):
        logger.debug("Found MacOs specific files. Removing...")
        shutil.rmtree(macosx_dir_path)


def contains_subdirectory(parent_dir: str):
    for name in os.listdir(parent_dir):
        if os.path.isdir(os.path.join(parent_dir, name)):
            return True
    return False


def delete_folder(folder_path: str):
    shutil.rmtree(folder_path)
