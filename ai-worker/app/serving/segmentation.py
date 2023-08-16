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
        image = Image.open(BytesIO(base64.b64decode(body["image"]))).convert("RGB")
        dataset_metadata = body["metadata"]
        dimensions = dataset_metadata["dimension"]
        transform = A.Compose(
            [
                A.Resize(height=256, width=256),
                ToTensorV2(),
            ]
        )
        data = transform(image=np.array(image))["image"]
        return np.array([data.numpy()]).astype(np.float32)

    def postprocess(
        self, data: Any, state: dict, collect_custom_statistics_fn=None
    ) -> Any:
        # post process the data returned from the model inference engine
        # data is the return value from model.predict we will put is inside a return value as Y
        if not isinstance(data, np.ndarray):
            # this should not happen
            return dict(digit=-1)
        binary_masks = (data > 0.5).astype(np.uint8)
        pred = binary_masks[0]
        return dict(
            propabilities=[
                dict(
                    mask=base64.b64encode(binary_masks).decode(),
                    width=pred.shape[1],
                    height=pred.shape[2],
                )
            ]
        )
