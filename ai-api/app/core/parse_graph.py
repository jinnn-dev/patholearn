from typing import List, Optional
from app.schema.task import Graph, INode, NodeType
import networkx
from app.utils.logger import logger
import networkx as nx
import matplotlib.pyplot as plt
import os


def find_node_by_id(nodes: List[INode], id: str) -> Optional[INode]:
    return next((node for node in nodes if node.id == id), None)


def find_node_by_type(nodes: List[INode], node_type: NodeType) -> Optional[INode]:
    return next((node for node in nodes if NodeType(node.type) == node_type), None)


def parse_graph(builderState: Graph):
    graph = nx.DiGraph()
    for node in builderState.nodes:
        graph.add_node(
            node.id,
        )
        graph.nodes[node.id]["data"]: INode = node

    for conn in builderState.connections:
        graph.add_edge(conn.source, conn.target)

    graph = graph.to_directed()

    dataset_node = find_node_by_type(builderState.nodes, NodeType.DatasetNode)
    output_node = find_node_by_type(builderState.nodes, NodeType.OutputNode)

    for node in graph.nodes(data=True):
        node_data: INode = node[1]["data"]
        node_data.type = NodeType(node_data.type)
        parse_layer(node_data)

    nx.draw(graph)
    plt.savefig("/app/core/graph.png")
    plt.clf()


def parse_dataset_node(node: INode):
    pass


def parse_layer(node: INode):
    logger.debug(node.type == NodeType.Conv2DNode)
