from typing import List, Optional, Tuple, Union
from app.core.parser.parse_layer import (
    Add,
    Concatenate,
    get_torch_layer_string,
    get_torch_prefix,
    parse_add_layer,
    parse_concatenate_layer,
    parse_layer,
    get_output_shape,
)
import networkx as nx
from app.core.parser.parse_graph import (
    AddNode,
    ArchitectureNode,
    ConcatenateNode,
    Conv2dLayer,
    DatasetNode,
    OutputNode,
    Node,
)
from app.utils.logger import logger
import torch
from torchvision.models import ResNet


def get_layer_string(
    layer: torch.nn.Module, node_data: Node = None, prefix: str = "torch.nn."
):
    if isinstance(node_data, ArchitectureNode):
        return f"""torchvision.models.get_model(name="{node_data.version}", weights={None if node_data.pretrained == 'No'  else '"DEFAULT"'})"""
    return prefix + get_torch_layer_string(layer)


def get_classification_layer(
    in_channels: int, classes: int, result: List, result_strings: List
):
    classification_layer = torch.nn.Linear(
        in_features=in_channels, out_features=classes
    )

    result.append(classification_layer)
    result_strings.append(get_layer_string(classification_layer))


def get_classification_model(
    graph: nx.DiGraph,
    path: List[Union[str, dict]],
    dataset_node: DatasetNode,
    architecture_node: Optional[ArchitectureNode],
    output_node: OutputNode,
):
    input_data_shape = (
        1,
        dataset_node.channels,
        dataset_node.dimension.x if dataset_node.dimension.x <= 256 else 256,
        dataset_node.dimension.y if dataset_node.dimension.y <= 256 else 256,
    )

    if architecture_node is not None:
        # result = parse_layer(
        #     architecture_node, dataset_node.channels, layer_data_shape=input_data_shape
        # )[0][0]

        # modules = list(result.children())[:-1]
        # model = torch.nn.Sequential(*modules, torch.nn.Flatten(start_dim=1, end_dim=-1))
        # output_shape = get_output_shape(model, input_data_shape)
        # logger.info(output_shape)
        result, result_strings, in_channels, layer_data = parse_network(
            path, graph, dataset_node.channels, layer_data_shape=input_data_shape
        )
        get_classification_layer(
            in_channels, dataset_node.classes, result, result_strings
        )
        return torch.nn.Sequential(*result), result_strings
    result, result_strings, in_channels, layer_data = parse_network(
        path, graph, dataset_node.channels, layer_data_shape=input_data_shape
    )

    get_classification_layer(in_channels, dataset_node.classes, result, result_strings)

    return torch.nn.Sequential(*result), result_strings


def parse_network(
    network, graph: nx.DiGraph, in_channels, layer_data_shape
) -> Tuple[List[torch.nn.Module], List[str], int, Tuple]:
    layers = []
    layer_strings = []
    current_in_channels = in_channels
    current_shape = layer_data_shape
    for element in network:
        if isinstance(element, dict):
            for node_id, paths in element.items():
                node_data = graph.nodes[node_id]["data"]
                (
                    splitting_layer_data,
                    splitting_in_channels,
                    splitting_shape,
                ) = parse_layer(node_data, current_in_channels, current_shape)
                if splitting_layer_data is not None:
                    layers += splitting_layer_data
                    for layer in splitting_layer_data:
                        prefix = get_torch_prefix(layer)
                        layer_strings.append(
                            get_layer_string(layer, node_data=node_data, prefix=prefix)
                        )

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
                    ) = parse_network(
                        path, graph, splitting_in_channels, splitting_shape
                    )
                    path_layers.append(torch.nn.Sequential(*path_layer))
                    seq_string = "torch.nn.Sequential(\n"
                    for layer in path_layer:
                        prefix = get_torch_prefix(layer)
                        seq_string += (
                            "    "
                            + get_layer_string(
                                layer, node_data=node_data, prefix=prefix
                            )
                            + ",\n"
                        )
                    seq_string += ")"

                    combined_in_channels += new_in_channels
                combine_node_id = paths["combine"]

                combine_node_data = graph.nodes[combine_node_id]["data"]
                if isinstance(combine_node_data, AddNode):
                    combined_layer, channels, shape = parse_add_layer(
                        path_layers, splitting_shape
                    )
                if isinstance(combine_node_data, ConcatenateNode):
                    logger.debug(f"New shape before concat: {new_shape}")
                    combined_layer, channels, shape = parse_concatenate_layer(
                        path_layers, splitting_shape
                    )
                    logger.debug(f"New shape after concat: {shape}")
                logger.info("HERE IS CONCAT")
                current_in_channels = channels
                current_shape = shape
                layers.append(combined_layer)
                prefix = get_torch_prefix(layer)
                layer_strings.append(
                    get_layer_string(
                        combined_layer,
                        node_data=node_data,
                        prefix=prefix,
                    )
                )
                # current_in_channels = combined_in_channels
                # current_shape = new_shape

        else:
            node_id = element
            node_data = graph.nodes[node_id]["data"]
            layer_data, current_in_channels, current_shape = parse_layer(
                node_data, current_in_channels, current_shape
            )

            if layer_data is not None:
                layers += layer_data
                for layer in layer_data:
                    prefix = get_torch_prefix(layer)
                    layer_strings.append(
                        get_layer_string(layer, node_data=node_data, prefix=prefix)
                    )

    return layers, layer_strings, current_in_channels, current_shape
