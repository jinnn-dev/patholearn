import os
import uuid
from typing import Dict, List, Tuple

import numpy as np
from app.config import Config
from app.utils.slide_utils import delete_keys_from_dict
from PIL import Image
from pydicom import dcmread
from pydicom.pixel_data_handlers.util import apply_color_lut


class Dicom:
    @staticmethod
    def save_dicom_frames(
        path_to_dicom: str, folder_name: str
    ) -> Tuple[List[str], Dict]:
        frame_uuids = []

        ds = dcmread(path_to_dicom)

        photo_metric_interpretation = ds[0x0028, 0x0004].value

        pixel_arr = ds.pixel_array
        series_shape = pixel_arr.shape
        color_space = "L"

        if photo_metric_interpretation == "PALETTE COLOR":
            pixel_arr = apply_color_lut(pixel_arr, ds)
            color_space = "RGB"

        if len(series_shape) < 3:
            pixel_arr = [pixel_arr]

        for i in range(len(pixel_arr)):
            frame = pixel_arr[i].astype(float)
            frame_scaled = (np.maximum(frame, 0) / frame.max()) * 255.0
            frame_scaled = np.uint8(frame_scaled)
            im = Image.fromarray(frame_scaled, color_space)

            frame_uuid = uuid.uuid4()
            os.mkdir(f"{Config.TEMP_IMAGES_FOLDER}/{folder_name}/{frame_uuid}")
            im.save(
                f"{Config.TEMP_IMAGES_FOLDER}/{folder_name}/{frame_uuid}/{frame_uuid}.jpeg"
            )

            frame_uuids.append(str(frame_uuid))

        metadata = delete_keys_from_dict(
            dict_del=ds.to_json_dict(), keys_to_delete=["InlineBinary"]
        )

        return frame_uuids, metadata
