from datetime import datetime

import shortuuid
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base
# noinspection PyUnresolvedReferences
from app.models.task_group import TaskGroup


class Course(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), unique=True)
    short_name = Column(String(length=255), index=True, default=shortuuid.uuid)
    description = Column(String(length=255), nullable=True)
    created = Column(DateTime, default=datetime.now)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="courses")
    members = relationship("User", secondary="coursemembers", back_populates="courses")
    task_groups = relationship("TaskGroup", cascade="all, delete-orphan")
