from typing import List, Tuple

import torch
import torchvision
import numpy as np
import math

from app.core.parser.parse_graph import (
    ActivationFunction,
    BatchNormNode,
    Conv2dLayer,
    DropoutNode,
    FlattenNode,
    LinearLayer,
    Node,
    PoolingLayer,
    ResNetNode,
)
from app.schema.parser import ActivationFunctionModule


class Conv2dSame(torch.nn.Conv2d):
    def calc_same_pad(self, i: int, k: int, s: int, d: int) -> int:
        return max((math.ceil(i / s) - 1) * s + (k - 1) * d + 1 - i, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        ih, iw = x.size()[-2:]

        pad_h = self.calc_same_pad(
            i=ih, k=self.kernel_size[0], s=self.stride[0], d=self.dilation[0]
        )
        pad_w = self.calc_same_pad(
            i=iw, k=self.kernel_size[1], s=self.stride[1], d=self.dilation[1]
        )

        if pad_h > 0 or pad_w > 0:
            x = torch.nn.functional.pad(
                x, [pad_w // 2, pad_w - pad_w // 2, pad_h // 2, pad_h - pad_h // 2]
            )
        return torch.nn.functional.conv2d(
            x,
            self.weight,
            self.bias,
            self.stride,
            self.padding,
            self.dilation,
            self.groups,
        )


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
                    (
                        ""
                        if isinstance(layer, Add) or isinstance(layer, Conv2dSame)
                        else "torch.nn."
                    )
                    + str(layer)
                    for layer in module
                )
                module_str = f"torch.nn.Sequential({layers_str})"
            else:
                module_str = str(module)
            module_strings.append(module_str)
        return f"Add({', '.join(module_strings)})"


class Concatenate(torch.nn.Module):
    def __init__(self, *modules) -> None:
        super().__init__()
        self.concate_modules = torch.nn.ModuleList(modules)

    def forward(self, x):
        return torch.cat([module(x) for module in self.concate_modules], dim=1)

    def __str__(self):
        module_strings = []
        for module in self.concate_modules:
            if isinstance(module, torch.nn.Sequential):
                layers_str = ", ".join(
                    ("" if isinstance(layer, Add) else "torch.nn.") + str(layer)
                    for layer in module
                )
                module_str = f"torch.nn.Sequential({layers_str})"
            else:
                module_str = str(module)
            module_strings.append(module_str)
        return f"Concatenate({', '.join(module_strings)})"


def parse_conv2d_layer(
    layer_data: Conv2dLayer, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    if layer_data.padding == "same":
        layer = Conv2dSame(
            in_channels=in_channels,
            out_channels=layer_data.out_features,
            kernel_size=layer_data.kernel_size,
            stride=layer_data.stride,
        )
    else:
        layer = torch.nn.Conv2d(
            in_channels=in_channels,
            out_channels=layer_data.out_features,
            kernel_size=layer_data.kernel_size,
            stride=layer_data.stride,
        )

    layer_data_shape

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
    layer = torch.nn.Dropout(p=layer_data.percentage / 100)
    return [layer], in_channels, layer_data_shape


def parse_batch_norm_node(
    layer_data: BatchNormNode, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    layer = torch.nn.BatchNorm2d(in_channels, momentum=layer_data.momentum)
    return [layer], in_channels, layer_data_shape


def parse_resnet_node(
    layer_data: ResNetNode, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    pretrained_layer = torchvision.models.get_model(
        layer_data.version, weights="DEFAULT" if layer_data.pretrained else None
    )

    modules = list(pretrained_layer.children())[:-1]
    layer = torch.nn.Sequential(*modules)
    output_shape = get_output_shape(layer, layer_data_shape)
    return [pretrained_layer], output_shape[1], output_shape


def get_activation_function(activation_function: ActivationFunction) -> torch.nn.Module:
    torch_activation_function = ActivationFunctionModule._member_map_[
        activation_function.name
    ].value
    if activation_function == ActivationFunction.LogSoftmax:
        return torch_activation_function(dim=1)
    return torch_activation_function()


def parse_add_layer(
    layers: List, input_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    layer = Add(*layers)
    output_shape = get_output_shape(layer, input_data_shape)
    return layer, output_shape[1], output_shape


def parse_concatenate_layer(
    layers: List, input_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    layer = Concatenate(*layers)
    output_shape = get_output_shape(layer, input_data_shape)
    return layer, output_shape[1], output_shape


def get_output_shape(model: torch.nn.Module, layer_dim: tuple) -> tuple:
    model.eval()
    output = model(torch.rand(*(layer_dim))).data.shape
    return output


parse_dict = {
    Conv2dLayer: parse_conv2d_layer,
    LinearLayer: parse_linear_layer,
    PoolingLayer: parse_pooling_layer,
    FlattenNode: parse_flatten_node,
    DropoutNode: parse_dropout_node,
    BatchNormNode: parse_batch_norm_node,
    ResNetNode: parse_resnet_node,
}


def parse_layer(
    layer_data: Node, in_channels: int, layer_data_shape: tuple
) -> List[torch.nn.Module]:
    if type(layer_data) not in parse_dict:
        return None, in_channels, layer_data_shape
    return parse_dict[type(layer_data)](layer_data, in_channels, layer_data_shape)
