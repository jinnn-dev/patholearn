from typing import List
import networkx as nx
from pydantic import BaseModel
from torchvision import datasets
from app.core.parse_graph import Dataset
from app.utils.logger import logger


class Element(BaseModel):
    id: str
    lines: List[str]
    imports: List[str]
    forward_call: List[str]


def parse_to_pytorch_graph(graph: nx.DiGraph):
    nodes = []
    for node in graph.nodes(data=True):
        nodes.append(node)
    edges = []
    for edge in graph.edges:
        edges.append(edge)
    logger.debug(nodes)
    logger.debug(edges)
    # dataset_node: Dataset = next(iter(graph.nodes(data=True)), None)[1]["data"]
    # dataset = datasets[dataset_node.name]
    # logger.debug(dataset)
