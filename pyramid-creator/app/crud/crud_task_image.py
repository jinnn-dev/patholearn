from app.crud.base import CRUDBase
from app.schemas.task_image import TaskImage, CreateTaskImage, UpdateTaskImage


class CRUDTaskImage(CRUDBase[TaskImage, CreateTaskImage, UpdateTaskImage]):
    pass


crud_task_image = CRUDTaskImage(TaskImage, "task_image_id")
