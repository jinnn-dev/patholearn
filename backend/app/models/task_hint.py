from app.db.base_class import Base
from app.schemas.task_hint import HintType
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Enum


class TaskHint(Base):
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("task.id"))
    order_position = Column(Integer, nullable=False)
    needed_mistakes = Column(Integer, default=3)
    content = Column(Text())
    hint_type = Column(Enum(HintType), default=HintType.TEXT)
    images = relationship("HintImage", cascade="all, delete-orphan")
