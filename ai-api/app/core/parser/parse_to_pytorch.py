from __future__ import annotations

from string import Template
from typing import List, Optional

from pydantic import BaseModel
from app.core.parser.parse_classification_model import get_classification_model
from app.core.parser.parse_lightning import LightningModel, SegmentationModel
from app.utils.logger import logger
from app.schema.parser import ArchitectureString
import networkx as nx

from app.core.parser.parse_graph import (
    AddNode,
    ArchitectureNode,
    ClassifierMapping,
    ConcatenateNode,
    DatasetNode,
    MetricNode,
    Node,
    SegmentationNode,
    OutputNode,
    parse_graph_to_networkx,
)
from app.schema.task import Graph, Task, TaskVersion
import black
import random


class PytorchModel(BaseModel):
    import_string: str
    clearml_string: Optional[str]
    dataset_class: str
    dataset_module_class: str
    model_class: Optional[str]
    lightning_model_class: str
    model_instance: Optional[str]
    dataset_instance: str
    lightning_model_instance: str
    lightning_trainer: str
    lightning_train: str
    lightning_test: str
    lightning_checkpoint: str
    ignore_clearml: bool = False

    def __str__(self) -> str:
        line_break = "\n\n"
        elements = []
        for key, value in self.dict().items():
            if value is not None and key != "ignore_clearml":
                elements.append(value)

        return format_string(line_break.join(elements))


class ClassificationDataset:
    def __init__(self, dataset: DatasetNode) -> None:
        with open(
            f"/app/core/parser/templates/{dataset.dataset_type}/dataset.txt", "r"
        ) as f:
            src = Template(f.read())
            replacements = {"dataset_id": dataset.dataset_clearml_id}
            self.dataset = src.substitute(replacements)


class DatasetModule:
    def __init__(self, dataset: DatasetNode) -> None:
        with open(
            f"/app/core/parser/templates/{dataset.dataset_type}/data_module.txt", "r"
        ) as f:
            self.dataset_module = f.read()

    def get_instance(self, batch_size: int = 32, inlcude_seed: bool = False):
        random_seed = random.randint(0, 10000)
        if inlcude_seed:
            return f"""DataModule(batch_size={batch_size}, split_seed={random_seed})"""
        else:
            return f"""DataModule(batch_size={batch_size})"""


class MNISTDataModule:
    def __init__(self) -> None:
        with open("/app/core/parser/templates/data_module.txt", "r") as f:
            self.dataset_module = f.read()

    def get_instance(self, data_dir: str = "./", batch_size: int = 32):
        return f"""MNISTDataModule(data_dir="{data_dir})"""


class ClassificationModel:
    def __init__(
        self,
        layers: List[str],
        architecture_node: Optional[ArchitectureNode],
    ) -> None:
        with open("/app/core/parser/templates/classification_model.txt", "r") as f:
            src = Template(f.read())
            if architecture_node is None:
                combined_layers = ",\n".join(layers)
                result_string = "torch.nn.Sequential(" + combined_layers + ")"
                replacements = {
                    "model": result_string,
                    "model_replace": "",
                    "modelfc": "",
                    "weights_download": "",
                    "weights_load": "",
                    "weights_replace": "",
                }
            else:
                replacements = {
                    "model": layers[0],
                    "weights_download": f"""path = StorageManager.get_local_copy(remote_url="s3://10.168.2.83:9000/clearml/weights/{architecture_node.version}_bhi.ckpt")"""
                    if architecture_node.pretrained == "Medical"
                    else "",
                    "weights_load": "model_weights = torch.load(path)"
                    if architecture_node.pretrained == "Medical"
                    else "",
                    "weights_replace": "self.model.load_state_dict(model_weights, strict=False)"
                    if architecture_node.pretrained == "Medical"
                    else "",
                    "model_replace": "self.model.avgpool = AdaptiveAvgPool2dCustom(output_size=self.model.avgpool.output_size)",
                    "modelfc": f"self.model.{ClassifierMapping[type(architecture_node)]} = torch.nn.Sequential("
                    + ",\n".join(layers[1:])
                    + ")",
                }

            self.model_class = src.substitute(replacements)

    def get_instance(self):
        return "ClassificationModel()"


def get_dataset_module(dataset_node: DatasetNode, output_node: OutputNode):
    dataset = ClassificationDataset(dataset=dataset_node)
    data_module = DatasetModule(dataset=dataset_node)
    data_module_instance = data_module.get_instance(batch_size=output_node.batch_size)

    return dataset.dataset, data_module.dataset_module, data_module_instance


def get_model(
    graph: nx.DiGraph,
    dataset_node: DatasetNode,
    output_node: OutputNode,
    architecture_node: Optional[ArchitectureNode],
    combine_nodes: List[str],
):
    if dataset_node.dataset_type == "segmentation":
        return
    path = []
    if len(dataset_node.to_nodes) > 1 or len(combine_nodes) > 0:
        if architecture_node is None:
            get_path_until_output(graph, dataset_node.id, path)
        else:
            get_path_until_output(graph, architecture_node.id, path)

    else:
        path = list(nx.dfs_preorder_nodes(graph, dataset_node.id))
    layers, layer_strings = get_classification_model(
        graph, path, dataset_node, architecture_node, output_node
    )
    model = ClassificationModel(layer_strings, architecture_node)
    return model.model_class, model.get_instance()


def get_path_until_output(graph: nx.DiGraph, start_node_id: str, path: List):
    if start_node_id is None:
        return
    if graph.out_degree(start_node_id) > 2:
        split_node = start_node_id
    else:
        path_until_split, split_node = get_path_until_split(graph, start_node_id)
        for path_node in path_until_split:
            if graph.in_degree(path_node) > 1:
                path_until_split.remove(path_node)
        path += path_until_split
    if split_node is not None:
        splitting_paths = get_splitting_paths(graph, split_node)
        if splitting_paths != {}:
            path.append(splitting_paths)
            combine_node = splitting_paths[split_node]["combine"]
            if combine_node is None:
                return
            path_until_split, split_node = get_path_until_split_or_combine(
                graph, combine_node
            )
            get_path_until_output(graph, split_node, path)


def get_splitting_paths(graph: nx.DiGraph, start_node_id: str):
    neighbours = [node for node in graph.neighbors(start_node_id)]
    paths = {}
    for neighbour in neighbours:
        path_until_split, split_node = get_path_until_split_or_combine(graph, neighbour)

        if split_node == None:
            return paths
        if start_node_id not in paths:
            paths[start_node_id] = {"paths": [], "combine": None}

        if graph.out_degree(split_node) > 1:
            next_split = get_splitting_paths(graph, split_node)
            path_until_split.append(next_split)
        paths[start_node_id]["paths"].append(path_until_split)
        split_node_instance = graph.nodes[split_node]["data"]
        if isinstance(split_node_instance, AddNode) or isinstance(
            split_node_instance, ConcatenateNode
        ):
            paths[start_node_id]["combine"] = split_node
    logger.info(graph.nodes(data=True)[start_node_id])
    logger.info("-----")
    return paths


def get_split_path(graph: nx.DiGraph, start_node_id: str, end_node_id: str):
    return nx.all_simple_paths(graph, start_node_id, end_node_id)


def get_path_until_split_or_combine(graph: nx.DiGraph, start_node_id: str):
    path = []
    split_node = None

    for node in nx.dfs_preorder_nodes(graph, start_node_id):
        if graph.out_degree(node) < 2 and graph.in_degree(node) < 2:
            path.append(node)
        else:
            split_node = node
            break
    return path, split_node


def get_path_until_split(graph: nx.DiGraph, start_node_id: str):
    path = []
    split_node = None
    for node in nx.dfs_preorder_nodes(graph, start_node_id):
        if graph.out_degree(node) < 2:
            path.append(node)
        else:
            split_node = node
            break
    return path, split_node


def parse_to_pytorch(
    graph: nx.DiGraph,
    dataset_node: DatasetNode,
    output_node: OutputNode,
    architecture_node: Optional[ArchitectureNode],
    combine_nodes: List[str],
    metric_nodes: List[MetricNode],
    task: Task,
    version: TaskVersion,
    ignore_clearml: bool = False,
):
    if architecture_node is not None and isinstance(
        architecture_node, SegmentationNode
    ):
        imports = [
            "import multiprocessing",
            "import lightning as pl",
            "import torch",
            "from clearml import Task, Dataset as ClearMlDataset, OutputModel",
            "from torch.utils.data import random_split, DataLoader, Dataset",
            "import albumentations as A",
            "import numpy as np",
            "import glob",
            "from sklearn.model_selection import train_test_split",
            "from PIL import Image",
            "from albumentations.pytorch import ToTensorV2",
            "from tqdm import tqdm",
            "import segmentation_models_pytorch as smp",
            "from lightning.pytorch.callbacks import LearningRateMonitor, ModelCheckpoint",
        ]

        import_string = "\n".join(imports)

        dataset_class, dataset_module_class, dataset_module_call = get_dataset_module(
            dataset_node, output_node
        )
        dataset_instance = "data_module" + " = " + dataset_module_call

        lightning_model = SegmentationModel(output_node, metric_nodes)
        lightning_model_class = lightning_model.model_class
        lightning_model_instance = lightning_model.get_instance(
            "lightning_model", architecture_node
        )
        lightning_trainer = lightning_model.trainer
        lightning_train = f"trainer.fit(model=lightning_model, datamodule=data_module)"
        lightning_test = f"trainer.test(model=lightning_model, datamodule=data_module)"
        with open("/app/core/parser/templates/segmentation/checkpoint.txt") as f:
            src = Template(f.read())
            width = dataset_node.dimension.x
            height = dataset_node.dimension.y

            replacements = {
                "arch": ArchitectureString[architecture_node.version],
                "encoder": architecture_node.encoderVersion,
                "channels": 3,
                "width": width if width <= 256 else 256,
                "height": height if height <= 256 else 256,
            }
            lightning_checkpoint = src.substitute(replacements)
        if not ignore_clearml:
            with open("/app/core/parser/templates/clearml.txt", "r") as f:
                src = Template(f.read())
                replacements = {"project_name": task.name, "task_name": version.id}
                clearml_string = src.substitute(replacements)
        pytorch_model = PytorchModel(
            import_string=format_string(import_string),
            clearml_string=None if ignore_clearml else format_string(clearml_string),
            dataset_class=format_string(dataset_class),
            dataset_module_class=format_string(dataset_module_class),
            model_class=None,
            lightning_model_class=format_string(lightning_model_class),
            model_instance=None,
            dataset_instance=format_string(dataset_instance),
            lightning_model_instance=format_string(lightning_model_instance),
            lightning_trainer=format_string(lightning_trainer),
            lightning_train=format_string(lightning_train),
            lightning_test=format_string(lightning_test),
            lightning_checkpoint=format_string(lightning_checkpoint),
        )
        formatted = str(pytorch_model)
        return formatted, pytorch_model
    nodes = []
    for node in graph.nodes(data=True):
        nodes.append(node)
    edges = []
    for edge in graph.edges:
        edges.append(edge)

    imports = [
        "import multiprocessing",
        "import glob",
        "import torch",
        "from torch.utils.data import random_split, DataLoader, Dataset",
        "import lightning as pl",
        "from lightning.pytorch.callbacks import ModelCheckpoint",
        "import albumentations as A",
        "from albumentations.pytorch import ToTensorV2",
        "from PIL import Image",
        "import numpy as np",
        "import torchvision",
        "import torchmetrics",
        "import math",
    ]
    if ignore_clearml:
        imports.append(
            "from clearml import Dataset as ClearmlDataset, StorageManager",
        )
    else:
        imports.append(
            "from clearml import Task, Dataset as ClearmlDataset, OutputModel, StorageManager",
        )

    import_string = "\n".join(imports)

    dataset_class, dataset_module_class, dataset_module_call = get_dataset_module(
        dataset_node, output_node
    )

    paragraph = "\n\n"
    import_string = "\n".join(imports)
    dataset_instance = "data_module" + " = " + dataset_module_call
    nodes: List[Node] = []

    model_class, model_call = get_model(
        graph, dataset_node, output_node, architecture_node, combine_nodes
    )
    model_instance = "model" + " = " + model_call

    lightning_model = LightningModel(dataset_node, output_node, metric_nodes)
    lightning_model_class = lightning_model.model_class
    lightning_model_instance = lightning_model.get_instance("lightning_model", "model")
    lightning_trainer = lightning_model.trainer
    lightning_train = f"trainer.fit(model=lightning_model, datamodule=data_module)"
    lightning_test = f"trainer.test(model=lightning_model, datamodule=data_module)"
    with open("/app/core/parser/templates/checkpoint.txt") as f:
        src = Template(f.read())
        width = dataset_node.dimension.x
        height = dataset_node.dimension.y
        replacements = {
            "channels": dataset_node.channels,
            "width": width if width <= 256 else 256,
            "height": height if height <= 256 else 256,
        }
        lightning_checkpoint = src.substitute(replacements)
    if not ignore_clearml:
        with open("/app/core/parser/templates/clearml.txt", "r") as f:
            src = Template(f.read())
            replacements = {"project_name": task.name, "task_name": version.id}
            clearml_string = src.substitute(replacements)
    pytorch_model = PytorchModel(
        import_string=format_string(import_string),
        clearml_string=None if ignore_clearml else format_string(clearml_string),
        dataset_class=format_string(dataset_class),
        dataset_module_class=format_string(dataset_module_class),
        model_class=format_string(model_class),
        lightning_model_class=format_string(lightning_model_class),
        model_instance=format_string(model_instance),
        dataset_instance=format_string(dataset_instance),
        lightning_model_instance=format_string(lightning_model_instance),
        lightning_trainer=format_string(lightning_trainer),
        lightning_train=format_string(lightning_train),
        lightning_test=format_string(lightning_test),
        lightning_checkpoint=format_string(lightning_checkpoint),
    )
    formatted = str(pytorch_model)

    return formatted, pytorch_model


async def parse_task_version_to_python(
    task: Task, task_version: TaskVersion, ignore_clearml=False
):
    (
        parsed_graph,
        dataset_node,
        output_node,
        architecture_node,
        combine_nodes,
        metric_nodes,
    ) = await parse_graph_to_networkx(task_version.graph)

    formatted, model = parse_to_pytorch(
        parsed_graph,
        dataset_node,
        output_node,
        architecture_node,
        combine_nodes,
        metric_nodes,
        task,
        task.versions[0],
        ignore_clearml,
    )
    return formatted, model, dataset_node.dataset_id, dataset_node.dataset_clearml_id


def format_string(value: str):
    return black.format_str(value, mode=black.Mode())
