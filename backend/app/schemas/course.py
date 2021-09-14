from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.schemas.task_group import TaskGroup, TaskGroupDetail
from app.schemas.user import User


class CourseBase(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    created: Optional[datetime] = None


class CourseCreate(CourseBase):
    name: str


class CourseUpdate(CourseBase):
    pass


class CourseInDBBase(CourseBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Course(CourseInDBBase):
    owner: Optional[User] = None
    is_member: Optional[bool] = False
    percentage_solved: Optional[float]
    task_count: Optional[int] = None
    correct_tasks: Optional[int] = None
    wrong_tasks: Optional[int] = None
    new_tasks: Optional[int] = 0


class CourseAll(Course):
    members: Optional[List[User]] = None
    task_groups: Optional[List[TaskGroupDetail]] = None


class CourseAdmin(Course):
    members: Optional[List[User]] = None
    task_groups: Optional[List[TaskGroup]] = None


class CourseDetail(Course):
    task_groups: Optional[List[TaskGroup]] = None


class CourseInDb(CourseInDBBase):
    pass
