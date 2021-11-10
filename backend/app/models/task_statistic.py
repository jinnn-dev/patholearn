from sqlalchemy import JSON, Column, ForeignKey, Integer, Numeric, text, DateTime

from app.db.base_class import Base


class TaskStatistic(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('task.id'), nullable=False)
    base_task_id = Column(Integer, ForeignKey('basetask.id'))
    solved_date = Column(DateTime, nullable=False)
    percentage_solved = Column(Numeric(5, 2), server_default=text("0"), default=0)
    solution_data = Column(JSON, nullable=False)
    task_result = Column(JSON, nullable=True)
