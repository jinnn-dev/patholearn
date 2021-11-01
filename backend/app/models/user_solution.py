from sqlalchemy import JSON, Column, ForeignKey, Integer, Numeric, text

from app.db.base_class import Base


class UserSolution(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    task_id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    percentage_solved = Column(Numeric(5, 2), server_default=text("0"), default=0)
    base_task_id = Column(Integer, ForeignKey('basetask.id'))
    task_group_id = Column(Integer, ForeignKey('taskgroup.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    solution_data = Column(JSON, nullable=False)
    task_result = Column(JSON, nullable=True)
    failed_attempts = Column(Integer, nullable=False, server_default=text("0"), default=0)
