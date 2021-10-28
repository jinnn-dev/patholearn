from enum import IntEnum
from typing import Any, List, Optional, Union

from app.schemas.polygon_data import AnnotationData, OffsetPolygonData
from app.schemas.task_hint import TaskHint
from pydantic import BaseModel


class TaskType(IntEnum):
    DRAWING = 0
    DRAWING_WITH_CLASS = 1
    IMAGE_SELECT = 2

class TaskAnnotationType(IntEnum):
    POINT = 0
    LINE = 1
    POLYGON = 2


class AnnotationGroup(BaseModel):
    name: str
    color: str


class AnnotationGroupUpdate(AnnotationGroup):
    oldName: str
    name: Optional[str]
    color: Optional[str]


class TaskStatus(IntEnum):
    CORRECT = 1000
    TOO_MANY_INPUTS = 1001
    TOO_LESS_INPUTS = 1002
    PARTIAL = 1003
    WRONG = 1004
    DUPLICATE_HIT = 1005
    WRONG_NAME = 1006
    INACCURATE = 1007
    INVALID = 1008


class AnnotationFeedback(BaseModel):
    id: Optional[str]
    status: Optional[TaskStatus]
    percentage: Optional[float]
    lines_outside: Optional[List[Any]]

class SelectImageFeedback(BaseModel):
    index: Optional[int]
    status: Optional[TaskStatus]

class TaskFeedback(BaseModel):
    task_id: Optional[int]
    task_status: Optional[TaskStatus]
    response_text: Optional[str]
    result_detail: Optional[Union[List[SelectImageFeedback], List[AnnotationFeedback]]]


class TaskBase(BaseModel):
    layer: int
    task_type: TaskType
    task_question: str
    knowledge_level: int
    min_correct: int
    annotation_type: TaskAnnotationType
    annotation_groups: Optional[List[AnnotationGroup]]
    hints: Optional[List[TaskHint]]
    can_be_solved: bool = True


class TaskCreate(TaskBase):
    solution: Optional[List[Union[AnnotationData, OffsetPolygonData]]]
    task_data: Optional[Union[List[AnnotationData], List[str]]]
    hints: Optional[List[TaskHint]] = []
    base_task_id: int
    can_be_solved: Optional[bool]


class TaskUpdate(TaskBase):
    task_id: Optional[int]
    layer: Optional[int]
    task_question: Optional[str]
    task_type: Optional[int]
    knowledge_level: Optional[int]
    min_correct: Optional[int]
    annotation_type: Optional[TaskAnnotationType]
    task_data: Optional[Any]
    solution: Optional[Any]
    annotation_groups: Optional[List[AnnotationGroup]]
    can_be_solved: Optional[bool]


class TaskInDBBase(TaskBase):
    id: Optional[int]
    base_task_id: Optional[int]

    class Config:
        orm_mode = True


class TaskInDB(TaskInDBBase):
    pass


class Task(TaskInDB):
    task_data: Optional[Any]
    user_solution: Optional[Any]
    solution: Optional[Any]
    percentage_solved: Optional[float]

    pass
