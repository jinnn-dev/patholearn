from typing import List

from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.task_hint import TaskHint
from app.schemas.task_hint import TaskHintCreate, TaskHintUpdate


class CRUDTaskHint(CRUDBase[TaskHint, TaskHintCreate, TaskHintUpdate]):
    pass

    def get_hints_by_task(self, db: Session, task_id: int, mistakes: int) -> List[TaskHint]:
        """
        Returns all hints that should be shown for the given mistake amount

        :param db: DB-Session
        :param task_id: Id of the task
        :param mistakes: Amount of mistakes
        :return: All found hints
        """
        result = db.query(self.model).filter(self.model.task_id == task_id).filter(
            self.model.needed_mistakes <= mistakes).order_by(asc(self.model.needed_mistakes)).all()

        return result


crud_task_hint = CRUDTaskHint(TaskHint)
