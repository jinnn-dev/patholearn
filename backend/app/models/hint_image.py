from sqlalchemy import Column, ForeignKey, Integer, String

from app.db import Base


class HintImage(Base):
    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String(length=255))
    task_hint_id = Column(Integer, ForeignKey('taskhint.id'))
