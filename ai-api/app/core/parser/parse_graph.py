from typing import Dict, List, Literal, Optional
from app.schema.dataset import Dataset, DatasetType

from pydantic import BaseModel
from app.schema.task import Graph, IConnection, INode, NodeType
from app.utils.logger import logger
import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum
from app.crud.dataset import get_dataset as get_db_dataset


class Node(BaseModel):
    id: str
    from_nodes: Optional[str]
    to_nodes: Optional[List[str]]


class FlattenNode(Node):
    pass


class ResNetNode(Node):
    pass


class DatasetDimension(BaseModel):
    x: int
    y: int


class DatasetNode(Node):
    name: str
    channels: int
    dimension: DatasetDimension
    classes: int
    dataset_type: DatasetType
    dataset_id: str


class Optimizer(Enum):
    Sgd = "SGD"
    RmsProp = "RMSprop"
    Adagrad = "Adagrad"
    Adam = "Adam"


class LossFunction(Enum):
    CrossEntropy = "Cross-Entropy"
    Mae = "MAE (L1)"
    Mse = "MSE"
    Hinge = "Hinge"
    Nll = "NLL"


class ActivationFunction(Enum):
    Identity = "None (Linear)"
    Sigmoid = "sigmoid"
    Tanh = "tanh"
    Relu = "relu"
    Softmax = "softmax"
    LogSoftmax = "log_softmax"


class Layer(Node):
    in_features: int
    out_features: int
    activation_function: ActivationFunction


class LinearLayer(Layer):
    pass


class Conv2dLayer(Layer):
    kernel_size: tuple
    stride: tuple


class PoolingLayer(Node):
    kernel_size: tuple
    stride: tuple
    type: Literal["max", "average"]


class DropoutNode(Node):
    percentage: float


class OutputNode(Node):
    optimizer: Optimizer
    loss_function: LossFunction
    learning_rate: float
    epoch: int
    batch_size: int


class BatchNormNode(Node):
    momentum: float


class AddNode(Node):
    pass


class ConcatenateNode(Node):
    pass


Metric = Literal[
    "Accuracy",
    "ROC AUC",
    "Average Precision",
    "Cohen Kappa",
    "F1 Score",
    "Precision",
    "Loss",
    "Epoch",
]


class MetricNode(Node):
    value: Metric


def find_node_by_id(nodes: List[INode], id: str) -> Optional[INode]:
    return next((node for node in nodes if node.id == id), None)


def find_node_by_type(nodes: List[INode], node_type: NodeType) -> Optional[INode]:
    return next((node for node in nodes if node[1]["data"].type == node_type), None)


async def parse_graph_to_networkx(version_graph: Graph):
    nodes_dict = {node.id: node for node in version_graph.nodes}
    processed_nodes = {}

    # parse node type to enum
    for node in version_graph.nodes:
        node.type = NodeType(node.type)

    start_node_id = None
    end_node_id = None

    for node in version_graph.nodes:
        if node.type == NodeType.DatasetNode and start_node_id is None:
            start_node_id = node.id
        if node.type == NodeType.OutputNode and end_node_id is None:
            end_node_id = node.id

        _, node_instance = await parse_node(
            node, nodes_dict, version_graph.connections, processed_nodes
        )

    graph = nx.DiGraph()

    for node_id in processed_nodes:
        graph.add_node(node_id, data=processed_nodes[node_id])

    for connection in version_graph.connections:
        graph.add_edge(connection.source, connection.target)

    paths_between_generator = nx.all_simple_paths(
        graph, source=start_node_id, target=end_node_id
    )

    nodes_between_set = set()
    combine_nodes = set()

    for path in paths_between_generator:
        for node in path:
            node_instance = graph.nodes[node]["data"]
            if isinstance(node_instance, AddNode) or isinstance(
                node_instance, ConcatenateNode
            ):
                combine_nodes.add(node_instance.id)
            nodes_between_set.add(node)
    path_graph: nx.DiGraph = graph.subgraph(nodes_between_set)

    # for node in path_graph.nodes(data=True):
    #     logger.debug(node)

    dataset_node = path_graph.nodes[start_node_id]["data"]
    output_node = path_graph.nodes[end_node_id]["data"]

    metric_nodes = []
    for node in processed_nodes:
        if isinstance(graph.nodes[node]["data"], MetricNode):
            metric_nodes.append(graph.nodes[node]["data"])
    return (
        path_graph,
        dataset_node,
        output_node,
        list(combine_nodes),
        list(metric_nodes),
    )


async def get_dataset(node: INode):
    selected_dataset = node.controls[0].value
    loaded_dataset = await get_db_dataset(selected_dataset["id"])

    return DatasetNode(
        id=node.id,
        name=loaded_dataset.name,
        channels=1 if loaded_dataset.metadata.is_grayscale else 3,
        classes=len(loaded_dataset.metadata.classes),
        dimension=loaded_dataset.metadata.dimension,
        dataset_type=loaded_dataset.dataset_type,
        dataset_id=loaded_dataset.clearml_dataset["id"],
    )


async def get_linear_node(node: INode):
    return LinearLayer(
        id=node.id,
        in_features=1,
        out_features=node.controls[0].value,
        activation_function=ActivationFunction(node.controls[1].value),
    )


async def get_conv_node(node: INode):
    return Conv2dLayer(
        id=node.id,
        in_features=1,
        out_features=node.controls[0].value,
        activation_function=ActivationFunction(node.controls[3].value),
        kernel_size=(
            node.controls[1].value["x"],
            node.controls[1].value["y"],
        ),
        stride=(node.controls[2].value["x"], node.controls[2].value["y"]),
    )


async def get_output_node(node: INode):
    controls = {control.key: control.value for control in node.controls}

    return OutputNode(
        id=node.id,
        optimizer=Optimizer(controls["optimizer"]),
        loss_function=LossFunction(controls["loss"]),
        learning_rate=controls["learningRate"],
        epoch=controls["epochs"],
        batch_size=controls["batchSize"],
    )


async def get_flatten_node(node: INode):
    return FlattenNode(id=node.id)


async def get_pooling_node(node: INode):
    # logger.debug(node.controls)
    return PoolingLayer(
        id=node.id,
        kernel_size=(
            node.controls[0].value["x"],
            node.controls[0].value["y"],
        ),
        stride=(node.controls[1].value["x"], node.controls[1].value["y"]),
        type=node.controls[2].value,
    )


async def get_dropout_node(node: INode):
    return DropoutNode(id=node.id, percentage=node.controls[0].value)


async def get_batch_norm_node(node: INode):
    return BatchNormNode(id=node.id, momentum=node.controls[0].value)


async def get_add_node(node: INode):
    return AddNode(id=node.id)


async def get_concatenate_node(node: INode):
    return ConcatenateNode(id=node.id)


async def get_metric_node(node: INode):
    return MetricNode(id=node.id, value=node.controls[0].value)


async def get_resnet_node(node: INode):
    return ResNetNode(id=node.id)


def get_to_nodes(node: INode, connections: List[IConnection]):
    to_nodes = []
    for connection in connections:
        if connection.source == node.id:
            to_nodes.append(connection.target)
    return to_nodes


def get_from_nodes(node: INode, connections: List[IConnection]):
    from_nodes = []
    for connection in connections:
        if connection.target == node.id:
            from_nodes.append(connection.source)
    return from_nodes


node_type_map = {
    NodeType.DatasetNode: get_dataset,
    NodeType.Conv2DNode: get_conv_node,
    NodeType.LinearNode: get_linear_node,
    NodeType.OutputNode: get_output_node,
    NodeType.FlattenNode: get_flatten_node,
    NodeType.PoolingNode: get_pooling_node,
    NodeType.DropoutNode: get_dropout_node,
    NodeType.BatchNormNode: get_batch_norm_node,
    NodeType.AddNode: get_add_node,
    NodeType.ConcatenateNode: get_concatenate_node,
    NodeType.MetricNode: get_metric_node,
    NodeType.ResNetNode: get_resnet_node,
}


async def parse_node(
    node: INode,
    nodes_dict: Dict[str, INode],
    connections: List[IConnection],
    processed_nodes: Dict[str, INode],
):
    if node.id not in processed_nodes:
        if node.type not in node_type_map:
            return None
        node_function = node_type_map[node.type]
        node_instance = await node_function(node)
        processed_nodes[node.id] = node_instance
        to_nodes = get_to_nodes(node, connections)
        from_nodes = get_from_nodes(node, connections)
        node_instance.to_nodes = to_nodes
        node_instance.from_nodes = from_nodes
    return processed_nodes, node_instance
