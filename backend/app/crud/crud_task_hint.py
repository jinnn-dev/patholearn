from app.crud.base import CRUDBase
from app.models.task_hint import TaskHint
from app.schemas.task_hint import  TaskHintCreate, TaskHintUpdate


class CRUDTaskHint(CRUDBase[TaskHint, TaskHintCreate, TaskHintUpdate]):
    pass

crud_task_hint = CRUDTaskHint(TaskHint)
