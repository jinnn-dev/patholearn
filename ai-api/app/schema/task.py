from datetime import datetime
from typing import Any, List, Literal, Optional, TypeVar, Union
from app.schema.base_mongo_model import BaseMongoModel

from bson import ObjectId
from app.schema.py_object_id import PyObjectId
from pydantic import BaseModel, Field

from enum import Enum


class NodeType(Enum):
    Conv2DNode = "Conv2DNode"
    LinearNode = "LinearNode"
    PoolingNode = "PoolingNode"
    DatasetNode = "DatasetNode"
    FlattenNode = "FlattenNode"
    DropoutNode = "DropoutNode"
    BatchNormNode = "BatchNormNode"
    AddNode = "AddNode"
    ConcatenateNode = "ConcatenateNode"
    OutputNode = "OutputNode"
    MetricNode = "MetricNode"


class ControlType(Enum):
    ActivationControl = "ActivationControl"
    DimensionControl = "DimensionControl"
    DropdownControl = "DropdownControl"
    NumberControl = "NumberControl"
    MetricConrol = "MetricControl"


class ISerializable(BaseModel):
    type: Any
    id: str


class IPort(ISerializable):
    label: Optional[str]
    key: str
    socket: dict = {"name": str}


class IControl(ISerializable):
    type: ControlType
    key: str
    value: Any

    class Config:
        use_enum_values = True


class IInputControl(IControl):
    inputType: Union[float, str]


class IConnection(BaseModel):
    id: str
    source: str
    sourceOutput: str
    target: str
    targetInput: str


class INodePosition(BaseModel):
    id: str
    x: float
    y: float


class DimensionOption(BaseModel):
    min: int
    max: int
    placeholder: str
    initialValue: Optional[int]


class IDimensionControl(IControl):
    value: dict = {"x": Optional[int], "y": Optional[int]}
    label: str
    xOptions: DimensionOption
    yOptions: DimensionOption


class IDropdownControl(IControl):
    values: List[Any]
    label: str


class INumberControl(IControl):
    min: int
    max: int
    label: str
    placeholder: str


ControlType = TypeVar(
    "ControlType",
    IDropdownControl,
    IDimensionControl,
    INumberControl,
    IInputControl,
    IControl,
)


class ISocket(BaseModel):
    input: Optional[str]
    output: Optional[str]


class INode(ISerializable):
    type: NodeType
    label: str
    inputs: List[IPort]
    outputs: List[IPort]
    controls: List[ControlType]
    sockets: ISocket
    lockStatus: Optional[Any]

    class Config:
        use_enum_values = True


class Graph(BaseModel):
    nodes: List[INode] = Field(...)
    connections: List[IConnection] = Field(...)
    positions: List[INodePosition] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "nodes": [],
                "connections": [],
                "positions": [],
            }
        }


TaskVersionStatus = Literal[
    "creating",
    "created",
    "in_progress",
    "stopped",
    "closed",
    "failed",
    "completed",
    "queued",
    "published",
    "publishing",
    "unknown",
]


class TaskVersion(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    graph: Graph = Field(...)
    clearml_id: Optional[str] = None
    creation_date: datetime = Field(...)
    status: Optional[TaskVersionStatus] = None
    status_message: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "9a201441-0d63-4d65-bd38-b2f14b700803",
                "builder": {},
                "clearml_id": None,
            }
        }


class TaskVersionNoGraph(TaskVersion):
    graph: Optional[Graph] = None


class UpdateTaskVersion(BaseModel):
    id: PyObjectId
    graph: Optional[Graph]


class Task(BaseMongoModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    creator_id: str = Field(...)
    project_id: PyObjectId = Field(default_factory=PyObjectId, alias="project_id")
    creation_date: datetime = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(...)
    versions: List[TaskVersion] = Field(...)
    lockStatus: Optional[dict] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "9a201441-0d63-4d65-bd38-b2f14b700803",
                "creator_id": "740f0751-eb93-414c-b5e0-5e2caa5cfcb2",
                "project_id": "8134ccd1e5f04ac4b2cf9a64e48e7907",
                "creation_date": "",
                "name": "Test",
                "description": "This is a description",
                "versions": [],
            }
        }


class TaskNoGraph(Task):
    versions: List[TaskVersionNoGraph]


class CreateTask(BaseModel):
    name: str
    description: Optional[str]
    project_id: str


class UdateTask(BaseModel):
    id: str
    name: str
    description: Optional[str]


class Info(BaseModel):
    id: str
    first_name: str
    last_name: str
    color: str


class Member(BaseModel):
    id: str
    info: Info


class LockElement(BaseModel):
    task_id: str
    element_id: str
    user_id: str


class UnlockElements(BaseModel):
    task_id: str
    element_ids: List[str]
