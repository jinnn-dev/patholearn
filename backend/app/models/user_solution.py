from sqlalchemy import Integer, Column, ForeignKey, JSON, Numeric

from app.db.base_class import Base


class UserSolution(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    task_id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    percentage_solved = Column(Numeric(5, 2), default=0.00)
    base_task_id = Column(Integer, ForeignKey('basetask.id'))
    task_group_id = Column(Integer, ForeignKey('taskgroup.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    solution_data = Column(JSON, nullable=False)
    task_result = Column(JSON, nullable=True)
