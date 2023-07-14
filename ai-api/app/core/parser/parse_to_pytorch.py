from __future__ import annotations

from string import Template
from typing import List, Optional

from pydantic import BaseModel
from app.core.parser.parse_classification_model import get_classification_model
from app.core.parser.parse_lightning import LightningModel
from app.utils.logger import logger

import networkx as nx

from app.core.parser.parse_graph import (
    AddNode,
    ArchitectureNode,
    ConcatenateNode,
    DatasetNode,
    MetricNode,
    Node,
    OutputNode,
    parse_graph_to_networkx,
)
from app.schema.task import Graph, Task, TaskVersion
import black


class PytorchModel(BaseModel):
    import_string: str
    clearml_string: Optional[str]
    dataset_class: str
    dataset_module_class: str
    model_class: str
    lightning_model_class: str
    model_instance: str
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


class CustomDataset:
    def __init__(self, dataset_id: str) -> None:
        with open("/app/core/parser/templates/dataset.txt", "r") as f:
            src = Template(f.read())
            replacements = {"dataset_id": dataset_id}
            self.dataset = src.substitute(replacements)


class DatasetModule:
    def __init__(self) -> None:
        with open("/app/core/parser/templates/data_module.txt", "r") as f:
            self.dataset_module = f.read()

    def get_instance(self, batch_size: int = 32):
        return f"""DataModule(batch_size={batch_size})"""


class MNISTDataModule:
    def __init__(self) -> None:
        with open("/app/core/parser/templates/data_module.txt", "r") as f:
            self.dataset_module = f.read()

    def get_instance(self, data_dir: str = "./", batch_size: int = 32):
        return f"""MNISTDataModule(data_dir="{data_dir}", batch_size={batch_size})"""


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
                replacements = {"model": result_string, "modelfc": ""}
            else:
                replacements = {
                    "model": layers[0],
                    "modelfc": "self.model.fc = torch.nn.Sequential("
                    + ",\n".join(layers[1:])
                    + ")",
                }
            self.model_class = src.substitute(replacements)

    def get_instance(self):
        return "ClassificationModel()"


def get_dataset_module(dataset_node: DatasetNode, output_node: OutputNode):
    dataset = CustomDataset(dataset_node.dataset_id)
    data_module = DatasetModule()
    data_module_instance = data_module.get_instance(batch_size=output_node.batch_size)

    return dataset.dataset, data_module.dataset_module, data_module_instance


def get_model(
    graph: nx.DiGraph,
    dataset_node: DatasetNode,
    output_node: OutputNode,
    architecture_node: Optional[ArchitectureNode],
    combine_nodes: List[str],
):
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
    ]
    if ignore_clearml:
        imports.append(
            "from clearml import Dataset as ClearmlDataset",
        )
    else:
        imports.append(
            "from clearml import Task, Dataset as ClearmlDataset, OutputModel",
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
        replacements = {
            "channels": dataset_node.channels,
            "width": dataset_node.dimension.x,
            "height": dataset_node.dimension.y,
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
    return formatted, model


def format_string(value: str):
    return black.format_str(value, mode=black.Mode())
