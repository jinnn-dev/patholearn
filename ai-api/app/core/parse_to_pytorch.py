from enum import Enum
from string import Template
from typing import List
import networkx as nx
from pydantic import BaseModel
from torchvision import datasets
from app.core.parse_graph import (
    BatchNormNode,
    Dataset,
    FlattenNode,
    Layer,
    LinearLayer,
    Node,
    OutputNode,
    Conv2dLayer,
    PoolingLayer,
    DropoutNode,
)
from app.utils.logger import logger
from app.schema.task import Task, TaskVersion
import torch
import numpy as np
import black


class Element(BaseModel):
    id: str
    lines: List[str]
    imports: List[str]
    forward_call: List[str]


class DatasetElement(BaseModel):
    class_name: str
    class_content: str


class ActivationFunctionModule(Enum):
    Identity = torch.nn.Identity
    Sigmoid = torch.nn.Sigmoid
    Tanh = torch.nn.Tanh
    Relu = torch.nn.ReLU
    Softmax = torch.nn.Softmax
    LogSoftmax = torch.nn.LogSoftmax


class ActivationFunctionString(Enum):
    Identity = "torch.nn.Identity()"
    Sigmoid = "torch.nn.Sigmoid()"
    Tanh = "torch.nn.Tanh()"
    Relu = "torch.nn.ReLU()"
    Softmax = "torch.nn.Softmax()"
    LogSoftmax = "torch.nn.LogSoftmax(dim=1)"


class LossFunctionModule(Enum):
    CrossEntropy = torch.nn.functional.cross_entropy
    Mae = torch.nn.functional.l1_loss
    Mse = torch.nn.functional.mse_loss
    Hinge = torch.nn.functional.hinge_embedding_loss
    Nll = torch.nn.functional.nll_loss


class LossFunctionString(Enum):
    CrossEntropy = "torch.nn.functional.cross_entropy"
    Mae = "torch.nn.functional.l1_loss"
    Mse = "torch.nn.functional.mse_loss"
    Hinge = "torch.nn.functional.hinge_embedding_loss"
    Nll = "torch.nn.functional.nll_loss"


class OptimizerModule(Enum):
    Sgd = torch.optim.SGD
    RmsProp = torch.optim.RMSprop
    Adagrad = torch.optim.Adagrad
    Adam = torch.optim.Adam


class OptimizerString(Enum):
    Sgd = "torch.optim.SGD"
    RmsProp = "torch.optim.RMSprop"
    Adagrad = "torch.optim.Adagrad"
    Adam = "torch.optim.Adam"


class MNISTDataModule:
    def __init__(self) -> None:
        with open("/app/core/templates/data_module.txt", "r") as f:
            self.dataset_module = f.read()

    def get_instance(self, data_dir: str = "./", batch_size: int = 32):
        return f"""MNISTDataModule(data_dir="{data_dir}", batch_size={batch_size})"""


class ClassificationModel:
    def __init__(
        self,
        layers: nx.DiGraph,
        dataset_node: Dataset,
        output_node: OutputNode,
        num_classes: int,
        grayscale=False,
    ) -> None:
        self.layers = layers
        if grayscale:
            in_channels = 1
        else:
            in_channels = 3

        dfs_nodes = list(nx.dfs_preorder_nodes(layers, dataset_node.id))

        layer_ids = dfs_nodes[1:-1]
        layer_data = [layers.nodes[layer_id]["data"] for layer_id in layer_ids]
        input_data_shape = (
            output_node.batch_size,
            in_channels,
            dataset_node.dimension.x,
            dataset_node.dimension.y,
        )

        logger.debug(input_data_shape)
        # logger.debug(layer_data)
        in_features = in_channels
        layer_data_shape = input_data_shape
        logger.debug(layer_data_shape)
        parsed_layers = []
        parsed_layers_strings = []
        for index, layer in enumerate(layer_data):
            if isinstance(layer, Conv2dLayer):
                parsed_layer_string = f"""torch.nn.Conv2d(in_channels={in_features}, out_channels={layer.out_features}, kernel_size={layer.kernel_size}, stride={layer.stride})"""
                parsed_layers_strings.append(parsed_layer_string)

                parsed_layer = torch.nn.Conv2d(
                    in_features,
                    out_channels=layer.out_features,
                    kernel_size=layer.kernel_size,
                    stride=layer.stride,
                )
                in_features = layer.out_features
                layer_data_shape = get_output_shape(parsed_layer, layer_data_shape)
                parsed_layers.append(parsed_layer)
                logger.debug(str(layer.activation_function))
                parsed_layers.append(
                    (
                        ActivationFunctionModule._member_map_[
                            layer.activation_function.name
                        ].value
                    )()
                )

                parsed_layers_strings.append(
                    ActivationFunctionString._member_map_[
                        layer.activation_function.name
                    ].value
                )

            if isinstance(layer, FlattenNode):
                parsed_layers_strings.append("torch.nn.Flatten()")
                parsed_layers.append(torch.nn.Flatten())

                in_features = np.prod(list(layer_data_shape)[1:])
            if isinstance(layer, LinearLayer):
                parsed_layer_string = f"""torch.nn.Linear(in_features={in_features}, out_features={layer.out_features})"""
                parsed_layers_strings.append(parsed_layer_string)

                parsed_layer = torch.nn.Linear(
                    in_features=in_features, out_features=layer.out_features
                )
                parsed_layers.append(
                    (
                        ActivationFunctionModule._member_map_[
                            layer.activation_function.name
                        ].value
                    )()
                )
                parsed_layers_strings.append(
                    (
                        ActivationFunctionString._member_map_[
                            layer.activation_function.name
                        ].value
                    )
                )
                in_features = layer.out_features
                parsed_layers.append(parsed_layer)
            if isinstance(layer, PoolingLayer):
                parsed_layer = None
                if layer.type == "average":
                    parsed_layer_string = f"torch.nn.AvgPool2d(kernel_size={layer.kernel_size}, stride={layer.stride})"
                    parsed_layer = torch.nn.AvgPool2d(
                        kernel_size=layer.kernel_size, stride=layer.stride
                    )
                else:
                    parsed_layer_string = f"torch.nn.MaxPool2d(kernel_size={layer.kernel_size}, stride={layer.stride})"
                    parsed_layer = torch.nn.MaxPool2d(
                        kernel_size=layer.kernel_size, stride=layer.stride
                    )
                layer_data_shape = get_output_shape(parsed_layer, layer_data_shape)
                logger.debug(layer_data_shape)
                parsed_layers_strings.append(parsed_layer_string)
            if isinstance(layer, DropoutNode):
                parsed_layer_string = f"torch.nn.Dropout(p={layer.percentage / 100})"
                parsed_layers_strings.append(parsed_layer_string)
            if isinstance(layer, BatchNormNode):
                parsed_layer_string = f"torch.nn.BatchNorm2d(num_features={in_features}, momentum={layer.momentum})"
                parsed_layers_strings.append(parsed_layer_string)
            else:
                continue
            parsed_layers.append(parsed_layer)

        logger.debug(parsed_layers)
        logger.debug(parsed_layers_strings)
        indent = " " * 12
        layers_string = ",\n".join(indent + line for line in parsed_layers_strings)
        sequential = f"""self.model = torch.nn.Sequential"""
        logger.debug(sequential)

        with open("/app/core/templates/classification_model.txt", "r") as f:
            src = Template(f.read())
            replacements = {"layers_string": layers_string}
            self.model_class = src.substitute(replacements)

        # for index in range(1, len(dfs_nodes) - 1):
        #     logger.debug(index)
        #     layer = layers.nodes[dfs_nodes[index]]["data"]
        #     parsed_layer = None

        #     if isinstance(layer, Conv2dLayer):
        #         parsed_layer = torch.nn.Conv2d(
        #             in_channels,
        #             out_channels=layer.out_features,
        #             kernel_size=layer.kernel_size,
        #             stride=layer.stride,
        #         )
        #         in_features = layer.out_features
        #     if isinstance(layer, FlattenNode):
        #         previous_layer = parsed_layers[index - 2]
        #         logger.debug(previous_layer)
        #         # in_features = get_output_shape()
        #         continue

        #     parsed_layers.append(parsed_layer)

        # features_end_index = -1
        # for i in range(len(layers)):
        #     if isinstance(layers[i], FlattenNode):
        #         features_end_index = i
        # logger.debug(layers)
        # for feature_index in range(features_end_index):
        #     logger.debug(layers[feature_index])

    def get_instance(self):
        return "ClassificationModel()"


class LightningModel:
    def __init__(self, output_node: OutputNode) -> None:
        self.learning_rate = output_node.learning_rate

        with open("/app/core/templates/lightning_model.txt", "r") as f:
            src = Template(f.read())
            replacements = {
                "learning_rate": self.learning_rate,
                "loss": LossFunctionString._member_map_[
                    output_node.loss_function.name
                ].value,
                "optimizer": OptimizerString._member_map_[
                    output_node.optimizer.name
                ].value,
            }
            result = src.substitute(replacements)
            self.model_class = result

        with open("/app/core/templates/trainer_instance.txt", "r") as f:
            src = Template(f.read())
            replacements = {"epochs": output_node.epoch}
            result = src.substitute(replacements)
            self.trainer = result

    def get_instance(self, model_name: str):
        return f"LightningModel({model_name})"


def parse_to_pytorch_graph(
    graph: nx.DiGraph,
    dataset_node: Dataset,
    output_node: OutputNode,
    task: Task,
    version: TaskVersion,
):
    nodes = []
    for node in graph.nodes(data=True):
        nodes.append(node)
    edges = []
    for edge in graph.edges:
        edges.append(edge)
    # logger.debug(nodes)
    # logger.debug(edges)

    imports = [
        "import sys",
        "import multiprocessing",
        "import torch",
        "import pytorch_lightning as pl",
        "import torchvision.datasets as datasets",
        "from torch.utils.data import random_split, DataLoader",
        "from torchvision import transforms",
        "import torchmetrics",
        "from clearml import Task",
    ]

    # logger.debug(output_node)

    import_string = "\n".join(imports)
    # logger.debug(import_string)

    dataset_class, dataset_call = get_dataset_module(dataset_node, output_node)

    paragraph = "\n\n"
    import_string = "\n".join(imports)
    dataset_instance = "data_module" + " = " + dataset_call
    nodes: List[Node] = []

    model_class, model_call = get_model(graph, dataset_node, output_node)
    model_instance = "model" + " = " + model_call

    lightning_model = LightningModel(output_node)
    lightning_model_class = lightning_model.model_class
    lightning_model_instance = "lightning_model = " + lightning_model.get_instance(
        "model"
    )
    lightning_trainer = "trainer = " + lightning_model.trainer
    lightning_train = f"trainer.fit(model=lightning_model, datamodule=data_module)"

    with open("/app/core/templates/clearml.txt", "r") as f:
        src = Template(f.read())
        replacements = {"project_name": task.name, "task_name": version.id}
        clearml_string = src.substitute(replacements)

    formated = black.format_str(
        import_string
        + paragraph
        + clearml_string
        + paragraph
        + dataset_class
        + paragraph
        + model_class
        + paragraph
        + lightning_model_class
        + paragraph
        + model_instance
        + paragraph
        + dataset_instance
        + paragraph
        + lightning_model_instance
        + paragraph
        + lightning_trainer
        + paragraph
        + lightning_train,
        mode=black.Mode(),
    )

    return formated


def get_dataset_module(dataset_node: Dataset, output_node: OutputNode):
    dataset_name = dataset_node.name
    if dataset_name == "MNIST":
        module = MNISTDataModule()
        instance = module.get_instance(data_dir="./", batch_size=output_node.batch_size)
        return module.dataset_module, instance
    return None, None


def get_model(graph: nx.digraph, dataset_node: Dataset, output_node: OutputNode):
    # for node in graph.nodes(data=True):
    #     logger.debug(node)
    model = ClassificationModel(
        graph, dataset_node, output_node, dataset_node.classes, True
    )
    return model.model_class, model.get_instance()


def get_output_shape(model: torch.nn.Module, image_dim: tuple):
    return model(torch.rand(*(image_dim))).data.shape
