from app.crud.base import CRUDBase
from app.schemas.task_hint import TaskHint, TaskHintCreate, TaskHintUpdate


class CRUDTaskHint(CRUDBase[TaskHint, TaskHintCreate, TaskHintUpdate]):
    pass
