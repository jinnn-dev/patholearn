import base64
from typing import Any


def convert_binary_to_base64(binary_data: bytes):
    return base64.b64encode(binary_data)

def is_byte_data(data: Any):
    return type(data) is bytes
