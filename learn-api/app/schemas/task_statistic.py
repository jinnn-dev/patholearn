from datetime import datetime
from typing import List, Union

from pydantic import BaseModel

from app.schemas.polygon_data import AnnotationData
from app.schemas.task import TaskFeedback


class TaskStatisticBase(BaseModel):
    user_id: int
    task_id: int
    base_task_id: int
    solved_date: datetime
    percentage_solved: float
    solution_data: Union[List[AnnotationData], List[str]]
    task_result: TaskFeedback


class TaskStatisticCreate(TaskStatisticBase):
    pass


class TaskStatisticUpdate(TaskStatisticBase):
    pass


class TaskStatisticInDB(TaskStatisticBase):
    id: int

    class Config:
        orm_mode = True


class TaskStatistic(TaskStatisticInDB):
    pass
