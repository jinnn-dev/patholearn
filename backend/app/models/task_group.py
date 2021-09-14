import shortuuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
# noinspection PyUnresolvedReferences
from app.models.base_task import BaseTask


class TaskGroup(Base):
    id = Column(Integer, primary_key=True, index=True)
    short_name = Column(String(length=255), index=True, default=shortuuid.uuid)
    name = Column(String(length=255))
    course_id = Column(Integer, ForeignKey('course.id'))
    tasks = relationship("BaseTask", cascade="all, delete-orphan")
