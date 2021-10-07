from typing import List

from app.crud.base import CRUDBase
from app.models.task_hint import TaskHint
from app.schemas.task_hint import TaskHintCreate, TaskHintUpdate
from sqlalchemy.orm import Session


class CRUDTaskHint(CRUDBase[TaskHint, TaskHintCreate, TaskHintUpdate]):
    pass

    def get_hints_by_task(self, db: Session, task_id: int, mistakes: int) -> List[TaskHint]:

        result = db.query(TaskHint).filter(TaskHint.task_id == task_id).filter(TaskHint.needed_mistakes <= mistakes).all()

        return result

crud_task_hint = CRUDTaskHint(TaskHint)
