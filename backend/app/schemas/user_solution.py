from typing import Optional, Any, List, Union

from pydantic import BaseModel

from app.schemas.polygon_data import AnnotationData
from app.schemas.task import TaskFeedback


class UserSolutionBase(BaseModel):
    percentage_solved: float
    solution_data: List[Union[AnnotationData]]
    task_result: Optional[TaskFeedback] = None


class UserSolutionCreate(BaseModel):
    task_id: int
    user_id: Optional[int]
    base_task_id: int
    task_group_id: int
    course_id: Optional[int]
    solution_data: Any
    task_result: Optional[TaskFeedback] = None


class UserSolutionUpdate(BaseModel):
    user_id: Optional[int]
    task_id: Optional[int]
    solution_data: Optional[Any]
    task_result: Optional[TaskFeedback]
    percentage_solved: Optional[float]


class UserSolutionInDB(UserSolutionBase):
    task_id: int
    base_task_id: int
    task_group_id: int
    course_id: int

    class Config:
        orm_mode = True


class UserSolution(UserSolutionInDB):
    pass
