from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.new_task import NewTask
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):

    def has_new_task(self, db: Session, user_id: int, base_task_id: int) -> bool:
        """
        Check if the base task has new tasks for the given user

        :param db: DB-Session
        :param user_id: ID of the user
        :param base_task_id: ID of the BaseTask
        :return: If there are new tasks or not
        """
        result = db.query(self.model).filter(self.model.base_task_id == base_task_id).filter(
            self.model.user_id == user_id).first()
        return True if result is not None else False

    def has_new_task_multiple_base_tasks(self, db: Session, user_id: int, base_task_ids: List[int]) -> bool:
        """
        Check if any of the base tasks has new tasks for the given user

        :param db: DB-Session
        :param user_id: ID of the user
        :param base_task_ids: Id of the BaseTask
        :return: Whether there are new tasks or not
        """
        result = db.query(self.model).filter(self.model.base_task_id.in_(base_task_ids)).filter(
            self.model.user_id == user_id).first()
        return True if result is not None else False

    def create_new_task(self, db: Session, user_id: int, base_task_id: int) -> NewTask:
        """
        Creates a new Entity which indicates that the given user has new tasks

        :param db: DB-Session
        :param user_id: ID of the user
        :param base_task_id: ID of the Base Task
        :return: The Entity representing that there is a new task
        """
        db_obj = NewTask()
        db_obj.user_id = user_id
        db_obj.base_task_id = base_task_id
        obj = db.add(db_obj)
        db.commit()
        return obj

    def remove_new_task(self, db: Session, user_id: int, base_task_id: int) -> NewTask:
        """
        Removes the entity for identifying that there is a new task for the user

        :param db: DB- Session
        :param user_id: ID of the user
        :param base_task_id: ID of the BaseTask
        :return: The deleted entity
        """
        obj = db.query(self.model).filter(self.model.base_task_id == base_task_id).filter(
            self.model.user_id == user_id).first()
        if obj is not None:
            db.delete(obj)
            db.commit()
        return obj

    def remove_all_to_task_id(self, db: Session, base_task_id: int) -> List[NewTask]:
        """
        Removes all identifications to the BastTask

        :param db: DB-Session
        :param base_task_id: ID of the base task
        :return: The deleted entities
        """
        db_objs = db.query(self.model).filter(self.model.base_task_id == base_task_id).all()
        for obj in db_objs:
            db.delete(obj)
        db.commit()
        return db_objs


crud_task = CRUDTask(Task)
