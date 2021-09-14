from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.base_task import BaseTask
from app.schemas.base_task import BaseTaskUpdate, BaseTaskCreate


class CRUDBaseTask(CRUDBase[BaseTask, BaseTaskCreate, BaseTaskUpdate]):

    def get_multi_by_task_group(self, db: Session, *, task_group_id: int) -> List[BaseTask]:
        """
        Returns all BaseTasks to the given TaskGroup.

        :param db: DB-Session
        :param task_group_id: id of the TaskGroup
        :return: All found TaskGroups
        """
        return db.query(self.model).filter(BaseTask.task_group_id == task_group_id).all()

    def get_multi_with_no_task_group(self, db: Session, *, course_id: int) -> List[BaseTask]:
        """
        Returns all BaseTasks without a TaskGroup to the given Course.

        :param db: DB-Session
        :param course_id: id of the Course
        :return: All found Courses
        """
        return db.query(self.model).filter(BaseTask.course_id == course_id).filter(
            BaseTask.task_group_id.is_(None)).all()

    def get_by_short_name(self, db: Session, *, short_name: str) -> BaseTask:
        """
        Returns the TaskGroup to the Shortname.

        :param db: DB-Session
        :param short_name: Shortname of the TaskGroup
        :return: The found TaskGroup
        """
        return db.query(self.model).filter(BaseTask.short_name == short_name).first()

    def create_with_slide_id(self, db: Session, *, task_in: BaseTaskCreate) -> BaseTask:
        """
        Creates a new TaskGroup.

        :param db: DB-Session
        :param task_in: contains all information to create a new BaseTask
        :return: the created BaseTask
        """
        db_obj = BaseTask()
        db_obj.task_group_id = task_in.task_group_id
        db_obj.slide_id = task_in.slide_id
        db_obj.name = task_in.name
        db.add(db_obj)
        db.commit()
        db_obj = db.refresh(db_obj)
        return db_obj

    def get_by_name(self, db: Session, name: str, task_group_id: int) -> Optional[BaseTask]:
        """
        Returns the BaseTask with the given name to a TaskGroup

        :param db: DB-Session
        :param name: Name of the BaseTask
        :param task_group_id: Id of the TaskGroup
        :return: the found BaseTask
        """
        return db.query(self.model).filter(BaseTask.name == name).filter(
            BaseTask.task_group_id == task_group_id).first()

    def base_task_uses_slide(self, db: Session, slide_id: str) -> bool:
        """
        Checks if a base task uses the given slide

        :param db: DB-Session
        :param slide_id: ID of the Slide
        :return: If the slide is used by any base task
        """
        return db.query(self.model).filter(BaseTask.slide_id == slide_id).first() is not None


crud_base_task = CRUDBaseTask(BaseTask)
