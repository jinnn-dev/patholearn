from typing import List, Tuple

import torch
import numpy as np

from app.core.parse_graph import (
    ActivationFunction,
    BatchNormNode,
    Conv2dLayer,
    DropoutNode,
    FlattenNode,
    LinearLayer,
    Node,
    PoolingLayer,
)
from app.schema.parser import ActivationFunctionModule
from app.utils.logger import logger


def parse_conv2d_layer(
    layer_data: Conv2dLayer, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    layer = torch.nn.Conv2d(
        in_channels=in_channels,
        out_channels=layer_data.out_features,
        kernel_size=layer_data.kernel_size,
        stride=layer_data.stride,
    )

    activation = get_activation_function(layer_data.activation_function)
    return (
        [layer, activation],
        layer.out_channels,
        get_output_shape(layer, layer_data_shape),
    )


def parse_linear_layer(
    layer_data: LinearLayer, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    layer = torch.nn.Linear(
        in_features=in_channels, out_features=layer_data.out_features
    )

    activation = get_activation_function(layer_data.activation_function)

    return (
        [layer, activation],
        layer.out_features,
        get_output_shape(layer, layer_data_shape),
    )


def parse_pooling_layer(
    layer_data: PoolingLayer, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    if layer_data.type == "average":
        layer = torch.nn.AvgPool2d(
            kernel_size=layer_data.kernel_size, stride=layer_data.kernel_size
        )
    else:
        layer = torch.nn.MaxPool2d(
            kernel_size=layer_data.kernel_size, stride=layer_data.stride
        )

    return [layer], in_channels, get_output_shape(layer, layer_data_shape)


def parse_flatten_node(
    layer_data: FlattenNode, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    layer = torch.nn.Flatten()
    in_channels = np.prod(list(layer_data_shape)[1:])
    return (
        [layer],
        np.prod(list(layer_data_shape)[1:]),
        (layer_data_shape[0], in_channels),
    )


def parse_dropout_node(
    layer_data: DropoutNode, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    layer = torch.nn.Dropout(p=layer_data / 100)
    return [layer], in_channels, layer_data_shape


def parse_batch_norm_node(
    layer_data: BatchNormNode, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    layer = torch.nn.BatchNorm2d(in_channels, momentum=layer_data.momentum)
    return [layer], in_channels, layer_data_shape


def get_activation_function(activation_function: ActivationFunction) -> torch.nn.Module:
    torch_activation_function = ActivationFunctionModule._member_map_[
        activation_function.name
    ].value
    if activation_function == ActivationFunction.LogSoftmax:
        return torch_activation_function(dim=1)
    return torch_activation_function()


def get_output_shape(model: torch.nn.Module, layer_dim: tuple) -> tuple:
    return model(torch.rand(*(layer_dim))).data.shape


parse_dict = {
    Conv2dLayer: parse_conv2d_layer,
    LinearLayer: parse_linear_layer,
    PoolingLayer: parse_pooling_layer,
    FlattenNode: parse_flatten_node,
    DropoutNode: parse_dropout_node,
    BatchNormNode: parse_batch_norm_node,
}


def parse_layer(
    layer_data: Node, in_channels: int, layer_data_shape: tuple
) -> List[torch.nn.Module]:
    if type(layer_data) not in parse_dict:
        return None, in_channels, layer_data_shape
    return parse_dict[type(layer_data)](layer_data, in_channels, layer_data_shape)
