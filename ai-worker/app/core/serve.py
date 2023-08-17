from clearml import Task, Dataset, Model
from app.utils.process import run_command
import requests
import base64
import numpy as np
from PIL import Image
from io import BytesIO


def serve_model(clearml_task: Task, dataset_id: str):
    dataset = Dataset.get(dataset_id=dataset_id)

    model = Model(clearml_task.output_models_id["model"])
    model.publish()

    metadata = dataset.get_metadata()
    channels = 1 if metadata["is_grayscale"] else 3
    dataset_type = metadata["dataset_type"]
    if dataset_type == "segmentation":
        command = [
            "clearml-serving",
            "model",
            "add",
            "--engine",
            "triton",
            "--input-size",
            "-1",
            "3",
            "-1",
            "-1",
            "--input-type",
            "float32",
            "--input-name",
            "input",
            "--output-size",
            "-1",
            "6",
            "-1",
            "-1",
            "--output-type",
            "float32",
            "--output-name",
            "output",
            "--endpoint",
            clearml_task.id,
            "--preprocess",
            "/app/serving/segmentation.py",
            "--model-id",
            model.id,
            "--aux-config",
            'platform="onnxruntime_onnx"',
            'default_model_filename="model.bin"',
        ]
    else:
        num_classes = len(metadata["classes"])

        command = [
            "clearml-serving",
            "model",
            "add",
            "--engine",
            "triton",
            "--input-size",
            "-1",
            str(channels),
            "-1",
            "-1",
            "--input-type",
            "float32",
            "--input-name",
            "input",
            "--output-size",
            "-1",
            str(num_classes),
            "--output-type",
            "float32",
            "--output-name",
            "output",
            "--endpoint",
            clearml_task.id,
            "--preprocess",
            "/app/serving/classification_grayscale.py"
            if channels == 1
            else "/app/serving/classification_color.py",
            "--model-id",
            model.id,
            "--aux-config",
            'platform="onnxruntime_onnx"',
            'default_model_filename="model.bin"',
        ]
    return run_command(command)


def remove_model(clearml_task_id: str):
    command = ["clearml-serving", "model", "remove", "--endpoint", clearml_task_id]
    return run_command(command)


def get_prediction(clearml_task_id: str, image_data: bytes, metadata: dict):
    encoded_image = base64.b64encode(image_data)
    result = requests.post(
        f"http://10.168.2.83:8080/serve/{clearml_task_id}",
        json={"image": encoded_image.decode(), "metadata": metadata},
        headers={"Content-Type": "application/json"},
    )
    data = result.json()
    if "detail" in data.keys():
        raise Exception("Did not work")
    return data["propabilities"][0]


def check_if_model_available(clearml_task_id: str, dataset_id: str):
    dataset = Dataset.get(dataset_id=dataset_id)
    metadata = dataset.get_metadata()
    channels = 1 if metadata["is_grayscale"] else 3

    if channels == 1:
        imarray = np.random.rand(100, 100) * 255
    else:
        imarray = np.random.rand(100, 100, 3) * 255
    im = Image.fromarray(imarray.astype("uint8")).convert("RGBA")
    im_bytes = BytesIO()
    im.save(im_bytes, "PNG")
    try:
        get_prediction(
            clearml_task_id=clearml_task_id,
            image_data=im_bytes.getvalue(),
            metadata=metadata,
        )
        return True
    except Exception:
        return False
