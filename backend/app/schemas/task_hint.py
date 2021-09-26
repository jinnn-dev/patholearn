from enum import IntEnum
from typing import List, Optional

from app.schemas.hint_image import HintImage
from pydantic import BaseModel


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
    images: Optional[List[HintImage]]

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
    images: Optional[List[HintImage]] = []

class TaskHintUpdate(TaskHintBase):
    content: Optional[str]
    hint_type: Optional[HintType]
    order_position: Optional[int]
    needed_mistakes: Optional[int]
    images: Optional[List[HintImage]]

class TaskHint(TaskHintInDb):
    pass
