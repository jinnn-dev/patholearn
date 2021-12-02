import json
from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.task_statistic import TaskStatistic
from app.schemas.task_statistic import TaskStatisticCreate, TaskStatisticUpdate, TaskStatistic as TaskStatisticSchema


class CRUDTaskStatistic(CRUDBase[TaskStatistic, TaskStatisticCreate, TaskStatisticUpdate]):

    def get_oldest_task_statistics_to_base_task_id(self, db: Session, *, base_task_id: int) -> [List[
        TaskStatisticSchema], List[int]]:
        sql = text("""SELECT ts.* FROM taskstatistic as ts
         join (SELECT user_id, task_id, min(solved_date) as smallest_date
               FROM taskstatistic
               where base_task_id = :base_task_id
               GROUP BY task_id, user_id) as smallest
              on ts.user_id = smallest.user_id and ts.task_id = smallest.task_id and
                 ts.solved_date = smallest.smallest_date;""")
        result = db.execute(sql, {"base_task_id": base_task_id}).fetchall()
        task_statistics = []

        task_ids = set()

        for row in result:
            task_statistics.append(
                TaskStatisticSchema(
                    id=row[0],
                    user_id=row[1],
                    task_id=row[2],
                    base_task_id=row[3],
                    solved_date=row[4],
                    percentage_solved=float(row[5]),
                    solution_data=json.loads(row[6]),
                    task_result=json.loads(row[7])
                )
            )
            task_ids.add(row[2])
        return task_statistics, task_ids

    def remove_all_by_task_id(self, db: Session, *, task_id: int) -> List[TaskStatistic]:
        db_objs = db.query(self.model).filter(self.model.task_id == task_id).all()
        for obj in db_objs:
            db.delete(obj)
            db.commit()
        return db_objs

    def remove_all_by_base_task_id(self, db: Session, *, base_task_id: int):
        db_objs = db.query(self.model).filter(self.model.base_task_id == base_task_id).all()
        for obj in db_objs:
            db.delete(obj)
            db.commit()
        return db_objs

crud_task_statistic = CRUDTaskStatistic(TaskStatistic)
