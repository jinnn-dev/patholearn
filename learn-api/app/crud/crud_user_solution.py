from typing import List, Tuple

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_solution import UserSolution
from app.schemas.user import UserInDBBase
from app.schemas.user_solution import (
    UserSolution as SchemaSolution,
)
from app.schemas.user_solution import UserSolutionCreate, UserSolutionUpdate
from app.models.user import User
from app.utils.logger import logger


class CRUDUserSolution(CRUDBase[UserSolution, UserSolutionCreate, UserSolutionUpdate]):
    def get_solution_and_user_to_task(
        self, db: Session, *, user_id: int, task_id: int
    ) -> UserSolution:
        """
        Returns the UserSolution and User to the given user and task.

        :param db: DB-Session
        :param user_id: if of the user
        :param task_id: id of the task
        :return: The found UserSolution
        """
        return (
            db.query(self.model, User)
            .filter(UserSolution.user_id == user_id)
            .filter(UserSolution.task_id == task_id)
            .join(User, User.id == UserSolution.user_id)
            .first()
        )

    def get_solution_to_task_and_user(
        self, db: Session, *, user_id: int, task_id: int
    ) -> UserSolution:
        """
        Returns the UserSolution to the given user and task.

        :param db: DB-Session
        :param user_id: if of the user
        :param task_id: id of the task
        :return: The found UserSolution
        """
        return (
            db.query(self.model)
            .filter(UserSolution.user_id == user_id)
            .filter(UserSolution.task_id == task_id)
            .first()
        )

    def get_user_solution_to_users(
        self, db: Session, *, task_id: int, user_ids: List[int]
    ):
        # return [
        #     user_id.user_id
        #     for user_id in db.query(UserSolution)
        #     .filter(self.model.task_id == task_id)
        #     .all()
        # ]
        return db.query(UserSolution).filter(self.model.task_id == task_id).all()

    def get_user_solution_info_and_user_to_task(self, db: Session, *, task_id: int):
        """
        Returns all user solutions infos to the given task

        :param db: DB-Session
        :param task_id: Id of the task
        :return All found user solutions info and users
        """
        return (
            db.query(User.firstname, User.lastname, User.id, UserSolution)
            .select_from(UserSolution)
            .join(User, self.model.user_id == User.id)
            .filter(self.model.task_id == task_id)
            .all()
        )

    def get_solution_to_task(
        self, db: Session, *, task_id: int
    ) -> List[SchemaSolution]:
        """
        Returns all user solutions to the given task

        :param db: DB-Session
        :param task_id: Id of the task
        :return: All found user solutions
        """
        return db.query(self.model).filter(UserSolution.task_id == task_id).all()

    def remove_by_user_id_and_task_id(
        self, db: Session, *, user_id: int, task_id: int
    ) -> SchemaSolution:
        """
        Removes Solution of the given user to the given task.

        :param db: DB-Session
        :param user_id: id of the user
        :param task_id: id of the task
        :return:
        """
        db_obj = (
            db.query(self.model)
            .filter(UserSolution.user_id == user_id)
            .filter(UserSolution.task_id == task_id)
            .first()
        )
        db.delete(db_obj)
        db.commit()
        return db_obj

    def remove_all_by_task_id(
        self, db: Session, *, task_id: int
    ) -> List[SchemaSolution]:
        """
        Removes all UserSolutions to the task.

        :param db: DB-Session
        :param task_id: id of the Task
        :return: The deleted UserSolutions
        """
        db_objs = db.query(self.model).filter(UserSolution.task_id == task_id).all()
        for obj in db_objs:
            db.delete(obj)
            db.commit()
        return db_objs

    def remove_all_by_user_to_course(
        self, db: Session, user_id: int, course_id: int
    ) -> List[SchemaSolution]:
        """
        Removes all UserSolution of the User to a Course.

        :param db: DB-Session
        :param user_id: Id of the User
        :param course_id: Id of the Course
        :return: The deleted UserSolution
        """
        db_objs = (
            db.query(self.model)
            .filter(UserSolution.course_id == course_id)
            .filter(UserSolution.user_id == user_id)
            .all()
        )
        for obj in db_objs:
            db.delete(obj)
        db.commit()
        return db_objs

    def remove_all_to_course(self, db: Session, course_id: int) -> List[SchemaSolution]:
        """
        Removes all UserSolutions to a Course
        :param db: DB-Session
        :param course_id: Id of the Course
        :return: The deleted UserSolutions
        """
        db_objs = db.query(self.model).filter(UserSolution.course_id == course_id).all()
        for obj in db_objs:
            db.delete(obj)
        db.commit()
        return db_objs

    def remove_all_to_task_group(
        self, db: Session, task_group_id: int
    ) -> List[SchemaSolution]:
        """
        Removes all UserSolutions to the TaskGroup
        :param db: DB-Session
        :param task_group_id: Id of the TaskGroup
        :return: The deleted UserSolutions
        """
        db_objs = (
            db.query(self.model)
            .filter(UserSolution.task_group_id == task_group_id)
            .all()
        )
        for obj in db_objs:
            db.delete(obj)
        db.commit()
        return db_objs

    def remove_all_to_base_task(
        self, db: Session, base_task_id: int
    ) -> List[SchemaSolution]:
        """
        Removes all UserSolutions to the BaseTask
        :param db: DB-Session
        :param base_task_id: Id of the BaseTask
        :return: The deleted UserSolutions
        """
        db_objs = (
            db.query(self.model).filter(UserSolution.base_task_id == base_task_id).all()
        )
        for obj in db_objs:
            db.delete(obj)
        db.commit()
        return db_objs

    def get_solved_percentage_to_task_group(
        self, db: Session, *, user_id: int, task_group_id: int
    ) -> Tuple:
        """
        Returns the percentage of the user solved tasks to the given TaskGroup.

        :param db: DB-Session
        :param user_id: id of the user
        :param task_group_id: id of the TaskGroup
        :return: Tuple with percentage as Decimal
        """
        query = (
            db.query(func.sum(self.model.percentage_solved).label("percentage_solved"))
            .filter(self.model.user_id == user_id)
            .filter(self.model.task_group_id == task_group_id)
        )
        return query.first()

    def get_solved_percentage_to_base_task(
        self, db: Session, *, user_id: int, base_task_id: int
    ) -> Tuple:
        """
        Returns the percentage of the user solved tasks to the given BaseTask.

        :param db: DB-Session
        :param user_id: id of the user
        :param base_task_id: id of the BaseTask
        :return: Tuple with the percentage as Decimal
        """
        return (
            db.query(func.sum(self.model.percentage_solved).label("percentage_solved"))
            .filter(self.model.user_id == user_id)
            .filter(self.model.base_task_id == base_task_id)
            .first()
        )

    def get_solved_percentage_to_course(
        self, db: Session, *, user_id: int, course_id: int
    ) -> int:
        """
        Returns the percentage of the user solved tasks to the given Course

        :param db: DB-Session
        :param user_id: id of the user
        :param course_id: id of the course
        :return: The solved percentage
        """
        return (
            db.query(func.sum(self.model.percentage_solved).label("percentage_solved"))
            .filter(self.model.user_id == user_id)
            .filter(self.model.course_id == course_id)
            .first()[0]
            or 0.0
        )

    def get_amount_of_correct_solutions_to_course(
        self, db: Session, *, user_id: int, course_id: int
    ) -> int:
        """
        Returns the amount correct solved tasks to the course

        :param db: DB-Session
        :param user_id: id of the user
        :param course_id: id of the course
        :return: The amount of correct solutions
        """
        return self.__get_amount_of_correct_solution(
            db, user_id=user_id, id_name="course_id", id_value=course_id
        )

    def get_amount_of_wrong_solutions_to_course(
        self, db: Session, *, user_id: int, course_id: int
    ) -> int:
        """
        Returns the amount wrong solved tasks to the course

        :param db: DB-Session
        :param user_id: id of the user
        :param course_id: id of the course
        :return: The amount auf wrong solutions
        """
        return self.__get_amount_of_wrong_solutions(
            db, user_id=user_id, id_name="course_id", id_value=course_id
        )

    def get_amount_of_correct_solutions_to_task_group(
        self, db: Session, *, user_id: int, task_group_id: int
    ) -> int:
        """
        Returns the amount correct solved tasks to the task group

        :param db: DB-Session
        :param user_id: id of the user
        :param task_group_id: id of the course
        :return: The amount of correct solutions
        """
        return self.__get_amount_of_correct_solution(
            db, user_id=user_id, id_name="task_group_id", id_value=task_group_id
        )

    def get_amount_of_wrong_solutions_to_task_group(
        self, db: Session, *, user_id: int, task_group_id: int
    ) -> int:
        """
        Returns the amount wrong solved tasks to the task group

        :param db: DB-Session
        :param user_id: id of the user
        :param task_group_id: id of the task group
        :return: The amount of wrong solutions
        """
        return self.__get_amount_of_wrong_solutions(
            db, user_id=user_id, id_name="task_group_id", id_value=task_group_id
        )

    def get_amount_of_correct_solutions_to_base_task(
        self, db: Session, *, user_id: int, base_task_id: int
    ) -> int:
        """
        Returns the amount correct solved tasks to the base task

        :param db: DB-Session
        :param user_id: id of the user
        :param base_task_id: id of the course
        :return: The amount of correct solutions
        """
        return self.__get_amount_of_correct_solution(
            db, user_id=user_id, id_name="base_task_id", id_value=base_task_id
        )

    def get_amount_of_wrong_solutions_to_base_task(
        self, db: Session, *, user_id: int, base_task_id: int
    ) -> int:
        """
        Returns the amount wrong solved tasks to the base task

        :param db: DB-Session
        :param user_id: id of the user
        :param base_task_id: id of the base task
        :return: The amount of wrong solutions
        """
        return self.__get_amount_of_wrong_solutions(
            db, user_id=user_id, id_name="base_task_id", id_value=base_task_id
        )

    def increment_failed_attempts(self, db: Session, user_id: int, task_id: int) -> int:
        model = self.get_solution_to_task_and_user(db, user_id=user_id, task_id=task_id)
        new_attempts = model.failed_attempts + 1
        model.failed_attempts = new_attempts
        db.add(model)
        db.commit()
        db.refresh(model)
        return new_attempts

    def __get_amount_of_wrong_solutions(
        self, db: Session, *, user_id: int, id_name: str, id_value: int
    ) -> int:
        return (
            db.query(func.count())
            .filter(self.model.user_id == user_id)
            .filter(getattr(self.model, id_name) == id_value)
            .filter(
                and_(
                    func.JSON_LENGTH(self.model.task_result) != 1,
                    self.model.percentage_solved != 1.00,
                )
            )
            .first()[0]
            or 0.0
        )

    def __get_amount_of_correct_solution(
        self, db: Session, user_id: int, id_name: str, id_value: int
    ) -> int:
        return (
            db.query(func.count())
            .filter(self.model.user_id == user_id)
            .filter(getattr(self.model, id_name) == id_value)
            .filter(self.model.percentage_solved == 1.00)
            .first()[0]
            or 0.0
        )


crud_user_solution = CRUDUserSolution(UserSolution)
