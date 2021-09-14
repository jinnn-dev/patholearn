from sqlalchemy import Column, String, Integer, CHAR, Float

from app.db.base_class import Base


class Slide(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), unique=True)
    file_id = Column(String(length=255), index=True)
    status = Column(CHAR(1))
    mag = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    mpp = Column(Float, nullable=True)
