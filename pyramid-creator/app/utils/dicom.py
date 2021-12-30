import os
import uuid

import numpy as np
from PIL import Image
from pydicom import dcmread


class Dicom:
    @staticmethod
    def save_dicom_frames(path_to_dicom: str, folder_name: str):
        frame_uuids = []

        ds = dcmread(path_to_dicom)
        print(ds)
        pixel_arr = ds.pixel_array
        series_shape = pixel_arr.shape

        if len(series_shape) == 3:
            for i in range(len(pixel_arr)):
                # plt.savefig(f"./data/{frame}", cmap=plt.cm.bone)
                frame = pixel_arr[i].astype(float)
                frame_scaled = (np.maximum(frame, 0) / frame.max()) * 255.0
                frame_scaled = np.uint8(frame_scaled)
                im = Image.fromarray(frame_scaled, 'L')
                frame_uuid = uuid.uuid4()
                os.mkdir(f"./data/{folder_name}/{frame_uuid}")
                im.save(f"./data/{folder_name}/{frame_uuid}/{frame_uuid}.jpeg")
                frame_uuids.append(str(frame_uuid))

        return frame_uuids
