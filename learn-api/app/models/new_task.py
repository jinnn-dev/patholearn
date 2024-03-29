from sqlalchemy import ForeignKey, Integer, Column, CHAR

from app.db.base_class import Base


class NewTask(Base):
    user_id = Column(CHAR(36), ForeignKey("user.id"), primary_key=True)
    base_task_id = Column(Integer, ForeignKey("basetask.id"), primary_key=True)
