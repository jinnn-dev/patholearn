from typing import Any, List, Optional, Union

from pydantic import BaseModel

from app.schemas.user import User
from app.schemas.polygon_data import AnnotationData
from app.schemas.task import TaskFeedback


class UserSolutionBase(BaseModel):
    percentage_solved: float
    solution_data: Union[List[AnnotationData], List[str]]
    task_result: Optional[TaskFeedback] = None
    failed_attempts: Optional[int] = 0


class UserSolutionCreate(BaseModel):
    task_id: int
    user_id: Optional[str]
    base_task_id: int
    task_group_id: int
    course_id: Optional[int]
    solution_data: Any
    task_result: Optional[TaskFeedback] = None


class UserSolutionUpdate(BaseModel):
    user_id: Optional[str]
    task_id: Optional[str]
    solution_data: Optional[Any]
    task_result: Optional[TaskFeedback]
    percentage_solved: Optional[float]


class UserSolutionInDB(UserSolutionBase):
    user_id: Optional[str]
    task_id: int
    base_task_id: int
    task_group_id: int
    course_id: int

    class Config:
        orm_mode = True


class UserSolution(UserSolutionInDB):
    pass


class UserSolutionWithUser(BaseModel):
    user_solution: UserSolution
    user: User
