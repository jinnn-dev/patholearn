from typing import List, Tuple
from app.utils.logger import logger

import torch
import torchvision
import numpy as np
import math
from functools import reduce
from operator import mul

from app.core.parser.parse_graph import (
    ActivationFunction,
    AlexnetNode,
    ArchitectureNode,
    BatchNormNode,
    Conv2dLayer,
    DropoutNode,
    FlattenNode,
    GoogleNetNode,
    LinearLayer,
    Node,
    PoolingLayer,
    ResNetNode,
    VggNode,
)
from app.schema.parser import ActivationFunctionModule


class Add(torch.nn.Module):
    def __init__(self, *modules):
        super().__init__()
        self.sum_modules = torch.nn.ModuleList(modules)

    def forward(self, x):
        first_in = self.sum_modules[0][0].in_channels
        second_in = self.sum_modules[1][0].in_channels

        if first_in != second_in:
            out = self.sum_modules[0](x)
            module_sum = out + sum(module(out) for module in self.sum_modules[1:])
            return module_sum
        return sum(module(x) for module in self.sum_modules)

    def __str__(self):
        module_strings = []
        for module in self.sum_modules:
            if isinstance(module, torch.nn.Sequential):
                layer_strings = []
                for layer in module:
                    prefix = get_torch_prefix(layer)
                    layer_string = get_torch_layer_string(layer)
                    layer_strings.append(prefix + layer_string)
                layers_str = ", ".join(layer_strings)
                module_str = f"torch.nn.Sequential({layers_str})"
            else:
                module_str = get_torch_layer_string(module)
            module_strings.append(module_str)
        return f"Add({', '.join(module_strings)})"


class Concatenate(torch.nn.Module):
    def __init__(self, *modules) -> None:
        super().__init__()
        self.concate_modules = torch.nn.ModuleList(modules)

    def forward(self, x):
        first_in = self.concate_modules[0][0].in_channels
        second_in = self.concate_modules[1][0].in_channels

        if first_in != second_in:
            out = self.concate_modules[0](x)
            outputs = [out]
            outputs += [module(out) for module in self.concate_modules[1:]]
            return torch.cat(outputs, dim=1)
        return torch.cat([module(x) for module in self.concate_modules], dim=1)

    def __str__(self):
        module_strings = []
        for module in self.concate_modules:
            if isinstance(module, torch.nn.Sequential):
                layer_strings = []
                for layer in module:
                    prefix = get_torch_prefix(layer)
                    layer_string = get_torch_layer_string(layer)
                    layer_strings.append(prefix + layer_string)
                layers_str = ", ".join(layer_strings)
                module_str = f"torch.nn.Sequential({layers_str})"
            else:
                module_str = get_torch_layer_string(module)
            module_strings.append(module_str)

        return f"Concatenate({', '.join(module_strings)})"


class MaxPool2dSame(torch.nn.MaxPool2d):
    def calc_same_pad(self, i: int, k: int, s: int, d: int) -> int:
        return max((math.ceil(i / s) - 1) * s + (k - 1) * d + 1 - i, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        ih, iw = x.size()[-2:]

        pad_h = self.calc_same_pad(
            i=ih, k=self.kernel_size[0], s=self.stride[0], d=self.dilation
        )
        pad_w = self.calc_same_pad(
            i=iw, k=self.kernel_size[1], s=self.stride[1], d=self.dilation
        )

        if pad_h > 0 or pad_w > 0:
            x = torch.nn.functional.pad(
                x, [pad_w // 2, pad_w - pad_w // 2, pad_h // 2, pad_h - pad_h // 2]
            )
        return torch.nn.functional.max_pool2d(
            x,
            self.kernel_size,
            self.stride,
            self.padding,
            self.dilation,
            self.ceil_mode,
            self.return_indices,
        )


class AvgPool2dSame(torch.nn.AvgPool2d):
    def calc_same_pad(self, i: int, k: int, s: int, d: int) -> int:
        return max((math.ceil(i / s) - 1) * s + (k - 1) * d + 1 - i, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        ih, iw = x.size()[-2:]

        pad_h = self.calc_same_pad(
            i=ih, k=self.kernel_size[0], s=self.stride[0], d=self.dilation
        )
        pad_w = self.calc_same_pad(
            i=iw, k=self.kernel_size[1], s=self.stride[1], d=self.dilation
        )

        if pad_h > 0 or pad_w > 0:
            x = torch.nn.functional.pad(
                x, [pad_w // 2, pad_w - pad_w // 2, pad_h // 2, pad_h - pad_h // 2]
            )
        return torch.nn.functional.avg_pool2d(
            x,
            self.kernel_size,
            self.stride,
            self.padding,
            self.ceil_mode,
            self.count_include_pad,
            self.divisor_override,
        )


# From: https://github.com/pytorch/pytorch/issues/42653#issuecomment-1168816422
class AdaptiveAvgPool2dCustom(torch.nn.Module):
    def __init__(self, output_size):
        super(AdaptiveAvgPool2dCustom, self).__init__()
        self.output_size = np.array(output_size)

    def forward(self, x: torch.Tensor):
        stride_size = np.floor(np.array(x.shape[-2:]) / self.output_size).astype(
            np.int32
        )
        kernel_size = np.array(x.shape[-2:]) - (self.output_size - 1) * stride_size
        avg = torch.nn.AvgPool2d(
            kernel_size=list(kernel_size), stride=list(stride_size)
        )
        x = avg(x)
        return x

    def __str__(self) -> str:
        return f"AdaptiveAvgPool2dCustom(output_size=({self.output_size[0]}, {self.output_size[1]}))"


def parse_conv2d_layer(
    layer_data: Conv2dLayer, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    layer = torch.nn.Conv2d(
        in_channels=in_channels,
        out_channels=layer_data.out_features,
        kernel_size=layer_data.kernel_size,
        stride=layer_data.stride,
        padding=layer_data.padding,
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
        if layer_data.padding == "same":
            layer = AvgPool2dSame(
                kernel_size=layer_data.kernel_size, stride=layer_data.kernel_size
            )
        else:
            layer = torch.nn.AvgPool2d(
                kernel_size=layer_data.kernel_size, stride=layer_data.kernel_size
            )
    else:
        if layer_data.padding == "same":
            layer = MaxPool2dSame(
                kernel_size=layer_data.kernel_size, stride=layer_data.stride
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


def parse_architecture_node(
    layer_data: ArchitectureNode, in_channels: int, layer_data_shape: tuple
):
    version = layer_data.version if layer_data.version != None else "googlenet"
    pretrained_layer = torchvision.models.get_model(
        version,
        weights=None if layer_data.pretrained == "No" else "DEFAULT",
    )
    modules = list(pretrained_layer.children())[:-1]
    last_layer = modules[-1]
    if isinstance(last_layer, torch.nn.AdaptiveAvgPool2d):
        new_last_layer = AdaptiveAvgPool2dCustom(last_layer.output_size)
        modules[-1] = new_last_layer
        pretrained_layer.avgpool = AdaptiveAvgPool2dCustom(last_layer.output_size)
    logger.info(modules)
    layer = torch.nn.Sequential(*modules, torch.nn.Flatten(start_dim=1))
    output_shape = get_output_shape(layer, layer_data_shape)
    logger.info(pretrained_layer)
    return [pretrained_layer], output_shape[1], output_shape


def parse_resnet_node(
    layer_data: ResNetNode, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    return parse_architecture_node(layer_data, in_channels, layer_data_shape)


def parse_vgg_node(
    layer_data: VggNode, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    return parse_architecture_node(layer_data, in_channels, layer_data_shape)


def parse_googlenet_node(
    layer_data: GoogleNetNode, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    layer_data.version = "googlenet"
    return parse_architecture_node(layer_data, in_channels, layer_data_shape)


def parse_alexnet_node(
    layer_data: AlexnetNode, in_channels: int, layer_data_shape: tuple
) -> Tuple[List[torch.nn.Module], int, Tuple]:
    layer_data.version = "alexnet"
    return parse_architecture_node(layer_data, in_channels, layer_data_shape)


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
    VggNode: parse_vgg_node,
    GoogleNetNode: parse_googlenet_node,
    AlexnetNode: parse_alexnet_node,
}


def parse_layer(
    layer_data: Node, in_channels: int, layer_data_shape: tuple
) -> List[torch.nn.Module]:
    if type(layer_data) not in parse_dict:
        return None, in_channels, layer_data_shape
    return parse_dict[type(layer_data)](layer_data, in_channels, layer_data_shape)


def get_torch_layer_string(layer: torch.nn.Module):
    if isinstance(layer, torch.nn.Conv2d):
        return f"""Conv2d({layer.in_channels}, {layer.out_channels}, kernel_size={layer.kernel_size}, stride={layer.stride}, padding={'"same"' if layer.padding == "same" else layer.padding})"""
    return str(layer)


def get_torch_prefix(layer: torch.nn.Module):
    return (
        ""
        if isinstance(layer, Add)
        or isinstance(layer, Concatenate)
        or isinstance(layer, MaxPool2dSame)
        or isinstance(layer, AvgPool2dSame)
        else "torch.nn."
    )
