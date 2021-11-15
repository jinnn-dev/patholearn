from typing import Optional

from pydantic import BaseModel


class TaskImage(BaseModel):
    name: str
    task_image_id: str
    label: Optional[str]


class CreateTaskImage(TaskImage):
    pass


class UpdateTaskImage(BaseModel):
    task_image_id: str
    name: Optional[str]
    label: Optional[str]
