from enum import Enum
from pydantic import BaseModel
from typing import List
import torch


class Element(BaseModel):
    id: str
    lines: List[str]
    imports: List[str]
    forward_call: List[str]


class DatasetElement(BaseModel):
    class_name: str
    class_content: str


class ActivationFunctionModule(Enum):
    Identity = torch.nn.Identity
    Sigmoid = torch.nn.Sigmoid
    Tanh = torch.nn.Tanh
    Relu = torch.nn.ReLU
    Softmax = torch.nn.Softmax
    LogSoftmax = torch.nn.LogSoftmax


class ActivationFunctionString(Enum):
    Identity = "torch.nn.Identity()"
    Sigmoid = "torch.nn.Sigmoid()"
    Tanh = "torch.nn.Tanh()"
    Relu = "torch.nn.ReLU()"
    Softmax = "torch.nn.Softmax()"
    LogSoftmax = "torch.nn.LogSoftmax(dim=1)"


class LossFunctionModule(Enum):
    CrossEntropy = torch.nn.functional.cross_entropy
    Mae = torch.nn.functional.l1_loss
    Mse = torch.nn.functional.mse_loss
    Hinge = torch.nn.functional.hinge_embedding_loss
    Nll = torch.nn.functional.nll_loss


class LossFunctionString(Enum):
    CrossEntropy = "torch.nn.functional.cross_entropy"
    Mae = "torch.nn.functional.l1_loss"
    Mse = "torch.nn.functional.mse_loss"
    Hinge = "torch.nn.functional.hinge_embedding_loss"
    Nll = "torch.nn.functional.nll_loss"


class OptimizerModule(Enum):
    Sgd = torch.optim.SGD
    RmsProp = torch.optim.RMSprop
    Adagrad = torch.optim.Adagrad
    Adam = torch.optim.Adam


class OptimizerString(Enum):
    Sgd = "torch.optim.SGD"
    RmsProp = "torch.optim.RMSprop"
    Adagrad = "torch.optim.Adagrad"
    Adam = "torch.optim.Adam"
