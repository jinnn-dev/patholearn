from typing import Optional, List

from pydantic import BaseModel

from app.schemas.slide import Slide
from app.schemas.task import Task


class BaseTaskBase(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    enabled: Optional[bool] = False


class BaseTaskCreate(BaseTaskBase):
    name: str
    slide_id: int
    course_id: int
    task_group_id: Optional[int] = None


class BaseTaskUpdate(BaseTaskBase):
    base_task_id: int
    name: Optional[str] = None
    slide_id: Optional[int] = None
    task_group_id: Optional[int] = None


class BaseTaskInDBBase(BaseTaskBase):
    id: Optional[int] = None
    slide_id: Optional[int] = None
    task_group_id: Optional[int] = None

    class Config:
        orm_mode = True


class BaseTaskInDB(BaseTaskInDBBase):
    pass


class BaseTask(BaseTaskInDB):
    slide: Optional[Slide] = None
    percentage_solved: Optional[float]
    task_count: Optional[int]
    new_tasks: Optional[int] = 0
    correct_tasks: Optional[int] = None
    wrong_tasks: Optional[int] = None


class BaseTaskDetail(BaseTask):
    task_group_id: Optional[int] = None
    task_group_short_name: Optional[str] = None
    tasks: Optional[List[Task]] = None
