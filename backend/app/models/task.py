from sqlalchemy import Column, Integer, JSON, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    layer = Column(Integer, nullable=False)
    base_task_id = Column(Integer, ForeignKey('basetask.id'))
    task_type = Column(Integer)
    annotation_type = Column(Integer, nullable=False)
    min_correct = Column(Integer, nullable=False, default=1)
    task_question = Column(String(length=255))
    knowledge_level = Column(Integer)
    solution = Column(JSON, nullable=True)
    task_data = Column(JSON, nullable=True)
    annotation_groups = Column(JSON, nullable=True)
    hints = relationship("TaskHint", cascade="all, delete-orphan", order_by="TaskHint.needed_mistakes")
