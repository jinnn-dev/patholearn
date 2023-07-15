from clearml import Task, Dataset, Model
from app.utils.process import run_command


def serve_model(clearml_task: Task, dataset_id: str):
    dataset = Dataset.get(dataset_id=dataset_id)
    metadata = dataset.get_metadata()
    channels = 1 if metadata["is_grayscale"] else 3
    num_classes = len(metadata["classes"])

    model = Model(clearml_task.output_models_id["model"])
    model.publish()

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
