import base64
import os
from typing import Any, Dict, List, Tuple

from app.schemas.slide import Slide


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


def convert_slide_binary_metadata_to_base64(slide: Slide) -> List[Slide]:
    """
    Converts all binary data contained in the slide metadata to base64
    """
    if slide.metadata is not None:
        for metadata_key, metadata_value in slide.metadata.items():
            if is_byte_data(metadata_value):
                slide.metadata[metadata_key] = convert_binary_to_base64(
                    metadata_value)
    return slide


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
                    slide.metadata[metadata_key] = convert_binary_to_base64(
                        metadata_value)
    return slides


def openslide_can_load(file_extension: str) -> bool:
    """
    Checks if the given file extension can be loaded by openslide.

    :param file_extension: The file extension should be checked
    :return: If the file extension can be loaded by openslide or not
    """
    OPENSLIDE_FORMATS = ["svs", "tif", "vms", "vmu",
                         "ndpi", "scn", "mrxs", "tiff", "svslide", "bif"]

    return file_extension.lower() in OPENSLIDE_FORMATS


def get_file_name_and_file_extension(file_name_with_extension: str) -> Tuple[str, str]:
    """
    Splits the extension of the file name

    :param: file name with extension
    :return: file name and file extension
    """
    return os.path.splitext(file_name_with_extension)


def remove_truth_values_from_dict(dict_to_be_filtered: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Removes all entries in the given dict which have 'True' as value

    :param: Dict to filter
    :return: Filtered dict
    """
    query = {}
    if dict_to_be_filtered:
        for key in dict_to_be_filtered:
            if not dict_to_be_filtered[key]:
                query[key] = dict_to_be_filtered[key]
    return query


def delete_keys_from_dict(dict_del: Dict, keys_to_delete: List[str]) -> Dict:
    """
    Delets the given keys from the given dict
    :param dict_del: dict to delete keys from
    :param keys_to_delete:  All Keys that should be deleted
    :return: The dict without the deleted keys
    """
    for k in keys_to_delete:
        try:
            del dict_del[k]
        except KeyError:
            pass
    for v in dict_del.values():
        if isinstance(v, dict):
            delete_keys_from_dict(v, keys_to_delete)

    return dict_del
