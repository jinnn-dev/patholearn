from app.schema.task import Graph
import networkx
from app.utils.logger import logger
import networkx as nx
import matplotlib.pyplot as plt
import os


def parse_graph(builderState: Graph):
    G = nx.DiGraph()
    for node in builderState.nodes:
        G.add_node(node["id"])

    for conn in builderState.connections:
        G.add_edge(conn["source"], conn["target"])
    logger.debug(G.number_of_edges())

    G = G.to_directed()
    nx.draw(G)
    plt.savefig("/app/core/graph.png")
    plt.clf()
