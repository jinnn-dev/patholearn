from typing import Dict, List, Optional

from pydantic import BaseModel
from app.schema.task import Graph, IConnection, INode, NodeType
import networkx
from app.utils.logger import logger
import networkx as nx
import matplotlib.pyplot as plt
import os
from enum import Enum

# https://towardsdatascience.com/pytorch-layer-dimensions-what-sizes-should-they-be-and-why-4265a41e01fd

# graph = nx.DiGraph()
# for node in builderState.nodes:
#     graph.add_node(
#         node.id,
#     )
#     node.type = NodeType(node.type)
#     graph.nodes[node.id]["data"]: INode = node

# for conn in builderState.connections:
#     graph.add_edge(conn.source, conn.target)

# dataset_node = find_node_by_type(graph.nodes(data=True), NodeType.DatasetNode)
# dataset_node_data: INode = dataset_node[1]["data"]

# # for node in graph.nodes(data=True):
# #     neighbours = list(graph.neighbors(node[0]))
# #     logger.debug("-----" + str(node[1]["data"].type) + "------")
# #     for neighbour in neighbours:
# #         logger.debug(graph.nodes[neighbour])

# parsed_graph = nx.DiGraph()

# for neighbour in dataset_neighbours:
#     parse_node()
#     logger.debug(graph.nodes[neighbour])

# output_node = find_node_by_type(graph.nodes(data=True), NodeType.OutputNode)

# start_node = output_node
# logger.debug(start_node)
# for neighbour in graph.neighbors(start_node[0]):
#     logger.debug("Neighbour" + neighbour)

# for node in graph.nodes(data=True):
#     # logger.debug(node)
#     node_data: INode = node[1]["data"]
#     parse_layer(node_data)

# nx.draw(graph)
# plt.savefig("/app/core/graph.png")
# plt.clf()


class Node(BaseModel):
    id: str


class DatasetDimension(BaseModel):
    x: int
    y: int


class Dataset(Node):
    name: str
    channels: int
    dimension: DatasetDimension


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
    Adam = "Adam"
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


class OutputNode(Node):
    optimizer: Optimizer
    loss_function: LossFunction
    learning_rate: float
    epoch: int
    batch_size: int


def find_node_by_id(nodes: List[INode], id: str) -> Optional[INode]:
    return next((node for node in nodes if node.id == id), None)


def find_node_by_type(nodes: List[INode], node_type: NodeType) -> Optional[INode]:
    return next((node for node in nodes if node[1]["data"].type == node_type), None)


def parse_graph(builderState: Graph):
    nodes_dict = {node.id: node for node in builderState.nodes}
    processed_nodes = {}

    # parse node type to enum
    for node in builderState.nodes:
        node.type = NodeType(node.type)

    start_node_id = None
    end_node_id = None

    for node in builderState.nodes:
        if node.type == NodeType.DatasetNode and start_node_id is None:
            parse_node(node, nodes_dict, builderState.connections, processed_nodes)
            start_node_id = node.id
        if node.type == NodeType.OutputNode and end_node_id is None:
            end_node_id = node.id
        if start_node_id is not None and end_node_id is not None:
            break

    for node in builderState.nodes:
        parse_node(node, nodes_dict, builderState.connections, processed_nodes)

    graph = nx.DiGraph()

    for node_id in processed_nodes:
        graph.add_node(node_id, data=processed_nodes[node_id])

    for connection in builderState.connections:
        graph.add_edge(connection.source, connection.target)

    paths_between_generator = nx.all_simple_paths(
        graph, source=start_node_id, target=end_node_id
    )
    nodes_between_set = {node for path in paths_between_generator for node in path}

    path_graph: nx.DiGraph = graph.subgraph(nodes_between_set)

    for node in path_graph.nodes(data=True):
        logger.debug(node)

    return path_graph


def parse_node(
    node: INode,
    nodes_dict: Dict[str, INode],
    connections: List[IConnection],
    processed_nodes: Dict[str, INode],
):
    if node.id not in processed_nodes:
        if node.type == NodeType.DatasetNode:
            node_instance = get_dataset(node)
        elif node.type == NodeType.Conv2DNode:
            node_instance = get_conv_node(node)
        elif node.type == NodeType.LinearNode:
            node_instance = get_linear_node(node)
        elif node.type == NodeType.OutputNode:
            node_instance = get_output_node(node)
        else:
            return
        processed_nodes[node.id] = node_instance

    return processed_nodes


def get_neighbours(node: INode, connections: List[IConnection]):
    pass


def get_dataset(node: INode):
    control_value = node.controls[0].value
    selected_dataset_name = (
        node.controls[0].values[0] if control_value is None else control_value
    )

    if selected_dataset_name == "MNIST":
        return Dataset(
            id=node.id, name="MNIST", channels=1, dimension=DatasetDimension(x=28, y=28)
        )
    return None


def get_linear_node(node: INode):
    return LinearLayer(
        id=node.id,
        in_features=1,
        out_features=node.controls[0].value,
        activation_function=ActivationFunction(node.controls[1].value),
    )


def get_conv_node(node: INode):
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


def get_output_node(node: INode):
    controls = {control.key: control.value for control in node.controls}

    return OutputNode(
        id=node.id,
        optimizer=Optimizer(controls["optimizer"]),
        loss_function=LossFunction(controls["loss"]),
        learning_rate=controls["learningRate"],
        epoch=controls["epochs"],
        batch_size=controls["batchSize"],
    )
