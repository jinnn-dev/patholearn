from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.hint_image import HintImageBase, HintImage


class HintType(IntEnum):
    TEXT = 0
    IMAGE = 1
    SOLUTION = 2


class TaskHintBase(BaseModel):
    task_id: int
    content: str
    order_position: int
    needed_mistakes: int
    hint_type: HintType
    images: Optional[List[HintImageBase]] = []


class TaskHintInDb(TaskHintBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class TaskHintCreate(TaskHintBase):
    task_id: int
    content: str
    order_position: Optional[int] = 0
    needed_mistakes: Optional[int] = 3
    hint_type: HintType
    images: Optional[List[HintImageBase]] = []


class TaskHintUpdate(TaskHintBase):
    content: Optional[str]
    hint_type: Optional[HintType]
    order_position: Optional[int]
    needed_mistakes: Optional[int]
    images: Optional[List[HintImageBase]]


class TaskHint(TaskHintInDb):
    pass
