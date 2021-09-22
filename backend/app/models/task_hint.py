import shortuuid
from app.db.base_class import Base
# noinspection PyUnresolvedReferences
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Enum


class TaskHint(Base):
    id = Column(Integer, primary_key=True, index=True)
    hint_type = Column(Enum)
    