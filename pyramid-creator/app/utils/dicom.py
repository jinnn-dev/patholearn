import os
import uuid

import numpy as np
from PIL import Image
from pydicom import dcmread
from pydicom.pixel_data_handlers.util import apply_color_lut
from pydicom.util.fixer import fix_mismatch


class Dicom:
    @staticmethod
    def save_dicom_frames(path_to_dicom: str, folder_name: str):
        frame_uuids = []

        ds = dcmread(path_to_dicom)
        # print(ds)

        photo_metric_interpretation = ds[0x0028, 0x0004].value

        pixel_arr = ds.pixel_array
        series_shape = pixel_arr.shape
        color_space = 'L'
        print("Color space: ", photo_metric_interpretation)
        if photo_metric_interpretation == 'PALETTE COLOR':
            pixel_arr = apply_color_lut(pixel_arr, ds)
            color_space = 'RGB'

        print(pixel_arr.shape)

        if len(series_shape) < 3:
            pixel_arr = [pixel_arr]

        for i in range(len(pixel_arr)):
            frame = pixel_arr[i].astype(float)
            frame_scaled = (np.maximum(frame, 0) / frame.max()) * 255.0
            frame_scaled = np.uint8(frame_scaled)
            im = Image.fromarray(frame_scaled, color_space)

            frame_uuid = uuid.uuid4()
            os.mkdir(f"./data/{folder_name}/{frame_uuid}")
            im.save(f"./data/{folder_name}/{frame_uuid}/{frame_uuid}.jpeg")

            frame_uuids.append(str(frame_uuid))

        return frame_uuids
