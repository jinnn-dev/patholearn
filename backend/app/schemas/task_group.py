from typing import Optional, List

from pydantic import BaseModel

from app.schemas.base_task import BaseTask, BaseTaskDetail


class TaskGroupBase(BaseModel):
    name: Optional[str] = None


class TaskGroupCreate(TaskGroupBase):
    course_id: int
    name: str


class TaskGroupUpdate(TaskGroupBase):
    name: Optional[str] = None


class TaskGroupInDB(TaskGroupBase):
    id: Optional[int] = None
    short_name: str

    class Config:
        orm_mode = True


class TaskGroup(TaskGroupInDB):
    tasks: Optional[List[BaseTask]] = None
    course_id: int
    percentage_solved: Optional[float]
    task_count: Optional[int]
    new_tasks: Optional[int] = 0
    correct_tasks: Optional[int] = None
    wrong_tasks: Optional[int] = None


class TaskGroupDetail(TaskGroup):
    course_short_name: Optional[str] = None
    tasks: Optional[List[BaseTaskDetail]] = None
