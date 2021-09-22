from typing import Optional, List

from pydantic import BaseModel

from enum import Enum

from app.schemas.hint_image import HintImage


class HintType(Enum):
    TEXT = 0
    IMAGE = 1
    SOLUTION = 2

class TaskHint(BaseModel):
    id: int
    task_id: int
    content: str
    order_position: int
    needed_mistakes: int
    hint_type: HintType
    images: Optional[List[HintImage]]


class TaskHintCreate(TaskHint):
    task_id: int
    content: str
    order_position: Optional[int]
    needed_mistakes: Optional[int]
    hint_type: HintType
    images: Optional[List[HintImage]]

class TaskHintUpdate(TaskHint):
    content: Optional[str]
    hint_type: Optional[HintType]
    images: Optional[List[HintImage]]
    order_position: Optional[int]
    needed_mistakes: Optional[int]
