from typing import Any

import numpy as np
from PIL import Image
import torch
from io import BytesIO
import base64
import albumentations as A
from albumentations.pytorch import ToTensorV2


class Preprocess(object):
    def __init__(self):
        pass

    def preprocess(
        self, body: dict, state: dict, collect_custom_statistics_fn=None
    ) -> Any:
        image = Image.open(BytesIO(base64.b64decode(body["image"]))).convert("RGB")
        dataset_metadata = body["metadata"]
        dimensions = dataset_metadata["dimension"]
        image_numpy = np.array(image)
        if dimensions["x"] > 256:
            dimensions["x"] = 256
        if dimensions["y"] > 256:
            dimensions["y"] = 256
        transform = A.Compose(
            [
                A.Resize(height=dimensions["y"], width=dimensions["x"]),
                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
                ToTensorV2(),
            ]
        )
        data = transform(image=np.array(image_numpy))["image"]
        return np.array([data.numpy()]).astype(np.float32)

    def postprocess(
        self, data: Any, state: dict, collect_custom_statistics_fn=None
    ) -> dict:
        if not isinstance(data, np.ndarray):
            return dict(digit=-1)
        data = torch.tensor(data)
        propabilities = torch.nn.functional.softmax(data, dim=1)
        return dict(propabilities=propabilities.tolist())
