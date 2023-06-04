from enum import Enum
from typing import List
import networkx as nx
from pydantic import BaseModel
from torchvision import datasets
from app.core.parse_graph import (
    Dataset,
    FlattenNode,
    Layer,
    LinearLayer,
    Node,
    OutputNode,
    Conv2dLayer,
)
from app.utils.logger import logger
import torch
import numpy as np


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
        self.dataset_module = """# Data Module for loading data and setting up data loaders
class MNISTDataModule(pl.LightningDataModule):
    def __init__(self, data_dir: str = "./", batch_size: int = 32):
        super().__init__()
        self.data_dir = data_dir
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
        self.batch_size = batch_size

    def prepare_data(self):
        # download
        datasets.MNIST(self.data_dir, train=True, download=True)
        datasets.MNIST(self.data_dir, train=False, download=True)

    def setup(self, stage: str):
        # Assign train/val datasets for use in dataloaders
        if stage == "fit":
            mnist_full = datasets.MNIST(self.data_dir, train=True, transform=self.transform)
            self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])

        # Assign test dataset for use in dataloader(s)
        if stage == "test":
            self.mnist_test = datasets.MNIST(self.data_dir, train=False, transform=self.transform)

        if stage == "predict":
            self.mnist_predict = datasets.MNIST(self.data_dir, train=False, transform=self.transform)

    def train_dataloader(self):
        return DataLoader(
                self.mnist_train, 
                batch_size=self.batch_size, 
                num_workers=multiprocessing.cpu_count(),  
                shuffle=True, 
                drop_last=True
            )

    def val_dataloader(self):
        return DataLoader(
                self.mnist_val, 
                batch_size=self.batch_size, 
                num_workers=multiprocessing.cpu_count(),  
                shuffle=False, 
                drop_last=False
            )

    def test_dataloader(self):
        return DataLoader(
                self.mnist_test, 
                batch_size=self.batch_size, 
                num_workers=multiprocessing.cpu_count(), 
                shuffle=False, 
                drop_last=False
            )

    def predict_dataloader(self):
        return DataLoader(
                self.mnist_predict, 
                batch_size=self.batch_size, 
                num_workers=multiprocessing.cpu_count(), 
                shuffle=False, 
                drop_last=False
            )
"""

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

            else:
                continue
            parsed_layers.append(parsed_layer)

        logger.debug(parsed_layers)
        logger.debug(parsed_layers_strings)
        indent = " " * 12
        layers_string = ",\n".join(indent + line for line in parsed_layers_strings)
        sequential = f"""self.model = torch.nn.Sequential"""
        logger.debug(sequential)

        self.model_class = f"""class ClassificationModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        {sequential}(
{layers_string}
        )
    def forward(self, x):
        logits = self.model(x)
        return logits
        """

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
        self.model_class = f"""class LightningModel(pl.LightningModule):
    def __init__(self, model):
        super().__init__()

        self.learning_rate = {self.learning_rate}
        # The inherited PyTorch module
        self.model = model

        # Save settings and hyperparameters to the log directory
        # but skip the model parameters
        self.save_hyperparameters(ignore=['model'])

        # Set up attributes for computing the accuracy
        self.train_acc = torchmetrics.Accuracy(task='multiclass', num_classes=10)
        self.valid_acc = torchmetrics.Accuracy(task='multiclass', num_classes=10)
        self.test_acc = torchmetrics.Accuracy(task='multiclass', num_classes=10)
        
    # Defining the forward method is only necessary 
    # if you want to use a Trainer's .predict() method (optional)
    def forward(self, x):
        return self.model(x)
        
    # A common forward step to compute the loss and labels
    # this is used for training, validation, and testing below
    def _shared_step(self, batch):
        features, true_labels = batch
        logits = self(features)
        loss = {LossFunctionString._member_map_[output_node.loss_function.name].value}(logits, true_labels)
        predicted_labels = torch.argmax(logits, dim=1)
        return loss, true_labels, predicted_labels

    def training_step(self, batch, batch_idx):
        loss, true_labels, predicted_labels = self._shared_step(batch)
        self.log("train_loss", loss)
        
        # To account for Dropout behavior during evaluation
        self.model.eval()
        with torch.no_grad():
            _, true_labels, predicted_labels = self._shared_step(batch)
        self.train_acc.update(predicted_labels, true_labels)
        self.log("train_acc", self.train_acc, on_epoch=True, on_step=False)
        self.model.train()
        return loss  # this is passed to the optimzer for training

    def validation_step(self, batch, batch_idx):
        loss, true_labels, predicted_labels = self._shared_step(batch)
        self.log("valid_loss", loss)
        self.valid_acc(predicted_labels, true_labels)
        self.log("valid_acc", self.valid_acc,
                    on_epoch=True, on_step=False, prog_bar=True)

    def test_step(self, batch, batch_idx):
        loss, true_labels, predicted_labels = self._shared_step(batch)
        self.test_acc(predicted_labels, true_labels)
        self.log("test_acc", self.test_acc, on_epoch=True, on_step=False)

    def configure_optimizers(self):
        optimizer = {OptimizerString._member_map_[output_node.optimizer.name].value}(self.parameters(),  lr=self.learning_rate)
        return optimizer
    """

        self.trainer = f"""pl.Trainer(
    max_epochs={output_node.epoch},
    accelerator="auto",  # Uses GPUs or TPUs if available
    devices="auto",  # Uses all available GPUs/TPUs if applicable
    log_every_n_steps=100
)
        """

    def get_instance(self, model_name: str):
        return f"LightningModel({model_name})"


def parse_to_pytorch_graph(
    graph: nx.DiGraph, dataset_node: Dataset, output_node: OutputNode
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

    clearml_string = """Task.add_requirements("/clearml.requirements.txt")
task: Task = Task.init(project_name="Builder Test", task_name="MNIST")
task.execute_remotely(queue_name="default", clone=False, exit_process=True)"""
    return (
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
        + lightning_train
    )


def get_dataset_module(dataset_node: Dataset, output_node: OutputNode):
    dataset_name = dataset_node.name
    if dataset_name == "MNIST":
        module = MNISTDataModule()
        instance = module.get_instance(data_dir="./", batch_size=output_node.batch_size)
        return module.dataset_module, instance
    return None, None


def get_model(graph: nx.digraph, dataset_node: Dataset, output_node: OutputNode):
    model = ClassificationModel(
        graph, dataset_node, output_node, dataset_node.classes, True
    )
    return model.model_class, model.get_instance()


def get_output_shape(model: torch.nn.Module, image_dim: tuple):
    return model(torch.rand(*(image_dim))).data.shape
