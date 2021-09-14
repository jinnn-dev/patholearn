import base64
from typing import Any, Dict, List

from app.db.database import Slide


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
