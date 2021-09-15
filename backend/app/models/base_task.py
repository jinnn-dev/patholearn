import shortuuid
from sqlalchemy import Integer, Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base
# noinspection PyUnresolvedReferences
from app.models.task import Task


class BaseTask(Base):
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    task_group_id = Column(Integer, ForeignKey("taskgroup.id"), nullable=True)
    enabled = Column(Boolean, default=False)
    name = Column(String(length=255), index=True)
    short_name = Column(String(length=255), index=True, default=shortuuid.uuid)
    slide_id = Column(String(length=255), index=True)
    tasks = relationship("Task", cascade="all, delete-orphan")
