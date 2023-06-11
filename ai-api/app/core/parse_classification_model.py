from typing import List, Union
from app.core.parse_layer import parse_layer
import networkx as nx
from app.core.parse_graph import DatasetNode, OutputNode
from app.utils.logger import logger
import torch


def get_classification_model(
    graph: nx.DiGraph,
    path: List[Union[str, dict]],
    dataset_node: DatasetNode,
    output_node: OutputNode,
):
    input_data_shape = (
        output_node.batch_size,
        dataset_node.channels,
        dataset_node.dimension.x,
        dataset_node.dimension.y,
    )

    result, result_strings, in_channels, layer_data = parse_network(
        path, graph, dataset_node.channels, layer_data_shape=input_data_shape
    )
    joined_strings = "\n".join(result_strings)
    logger.debug(f"Sequential layers: {result}")
    logger.debug(f"Sequential layers string: {joined_strings}")

    return torch.nn.Sequential(*result), result_strings


class Add(torch.nn.Module):
    def __init__(self, *modules):
        super().__init__()
        self.sum_modules = torch.nn.ModuleList(modules)

    def forward(self, x):
        return sum(module(x) for module in self.sum_modules)

    def __str__(self):
        module_strings = []
        for module in self.sum_modules:
            if isinstance(module, torch.nn.Sequential):
                layers_str = ", ".join(
                    ("" if isinstance(layer, Add) else "torch.nn.") + str(layer)
                    for layer in module
                )
                module_str = f"torch.nn.Sequential({layers_str})"
            else:
                module_str = str(module)
            module_strings.append(module_str)
        return f"Add({', '.join(module_strings)})"


def parse_network(network, graph: nx.DiGraph, in_channels, layer_data_shape):
    layers = []
    layer_strings = []
    current_in_channels = in_channels
    current_shape = layer_data_shape

    for element in network:
        if isinstance(element, dict):
            for node_id, paths in element.items():
                node_data = graph.nodes[node_id]["data"]
                splitting_layer_data, current_in_channels, current_shape = parse_layer(
                    node_data, current_in_channels, current_shape
                )
                if splitting_layer_data is not None:
                    layers += splitting_layer_data
                    for layer in splitting_layer_data:
                        layer_strings.append("torch.nn." + str(layer))

                path_layers = []
                combined_in_channels = 0
                for path in paths["paths"]:
                    path_in_channels = current_in_channels
                    path_shape = current_shape
                    (
                        path_layer,
                        path_layer_strings,
                        new_in_channels,
                        new_shape,
                    ) = parse_network(path, graph, path_in_channels, path_shape)
                    path_layers.append(torch.nn.Sequential(*path_layer))
                    seq_string = "torch.nn.Sequential(\n"
                    for layer in path_layer:
                        if isinstance(layer, Add):
                            prefix = ""
                        else:
                            prefix = "torch.nn."
                        seq_string += "    " + prefix + str(layer) + ",\n"
                    seq_string += ")"

                    combined_in_channels = new_in_channels

                combined_layer = Add(*path_layers)
                layers.append(combined_layer)
                layer_strings.append(str(combined_layer))
                current_in_channels = combined_in_channels
                current_shape = new_shape

        else:
            node_id = element
            node_data = graph.nodes[node_id]["data"]
            layer_data, current_in_channels, current_shape = parse_layer(
                node_data, current_in_channels, current_shape
            )
            if layer_data is not None:
                layers += layer_data
                for layer in layer_data:
                    layer_strings.append("torch.nn." + str(layer))

    return layers, layer_strings, current_in_channels, current_shape
