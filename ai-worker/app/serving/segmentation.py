import io
from typing import Any, Union

import numpy as np
from PIL import Image
import torch
from io import BytesIO
import base64
from clearml import StorageManager
import albumentations as A
from albumentations.pytorch import ToTensorV2


# Notice Preprocess class Must be named "Preprocess"
class Preprocess(object):
    def __init__(self):
        # set internal state, this will be called only once. (i.e. not per request)
        pass

    def preprocess(
        self, body: dict, state: dict, collect_custom_statistics_fn=None
    ) -> Any:
        images = body["image"]
        dataset_metadata = body["metadata"]
        dimensions = dataset_metadata["dimension"]

        batch = []
        for image in images:
            loaded_image = Image.open(BytesIO(base64.b64decode(body["image"]))).convert(
                "RGB"
            )
            image_numpy = np.array(loaded_image)
            transform = A.Compose(
                [
                    A.Resize(height=dimensions["y"], width=dimensions["x"]),
                    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
                    ToTensorV2(),
                ]
            )
            data = transform(image=np.array(image))["image"]
            batch.append(data.numpy())
        return np.array(batch).astype(np.float32)

    def postprocess(
        self, data: Any, state: dict, collect_custom_statistics_fn=None
    ) -> Any:
        # post process the data returned from the model inference engine
        # data is the return value from model.predict we will put is inside a return value as Y
        if not isinstance(data, np.ndarray):
            # this should not happen
            return dict(digit=-1)
        binary_masks = (data > 0.5).astype(np.uint8)
        pred = binary_masks
        encoded_images = []
        for mask in binary_masks:
            encoded_images.append(base64.b64encode(mask).decode())
        return dict(
            propabilities=[
                dict(
                    mask=encoded_images,
                    width=pred.shape[1],
                    height=pred.shape[2],
                )
            ]
        )
