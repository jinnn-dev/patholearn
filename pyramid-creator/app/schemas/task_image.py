from typing import Optional

from pydantic import BaseModel


class TaskImage(BaseModel):
    name: str
    task_image_id: str


class CreateTaskImage(TaskImage):
    pass

class UpdateTaskImage(BaseModel):
    name: Optional[str]
