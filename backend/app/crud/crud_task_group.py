from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.task_group import TaskGroup
from app.schemas.task_group import TaskGroupCreate, TaskGroupUpdate


class CRUDTaskGroup(CRUDBase[TaskGroup, TaskGroupCreate, TaskGroupUpdate]):

    def get_multi_by_course_id(self, db: Session, *, course_id: int) -> List[TaskGroup]:
        """
        Returns all TaskGroups to the given course.

        :param db: DB-Session
        :param course_id: id of the course
        :return: All found TaskGroups
        """
        return db.query(self.model).filter(TaskGroup.course_id == course_id).all()

    def get_by_short_name(self, db: Session, *, short_name: str) -> TaskGroup:
        """
        Returns the TaskGroup matching to the shortname.

        :param db: DB-Session
        :param short_name: short name of the TaskGroup
        :return: The found TaskGroup
        """
        return db.query(self.model).filter(TaskGroup.short_name == short_name).first()

    def get_by_name(self, db: Session, *, name: str, course_id: int) -> Optional[str]:
        """
        Returns the TaskGroup to the name in the given course.

        :param db: DB-Session
        :param name: Name of the TaskGroup
        :param course_id: Id of the Course
        :return: The found TaskGroup
        """
        return db.query(self.model).filter(TaskGroup.name == name).filter(TaskGroup.course_id == course_id).first()


crud_task_group = CRUDTaskGroup(TaskGroup)
