from sqlalchemy import Column, Integer, Boolean, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    firstname = Column(String(length=255))
    middlename = Column(String(length=255), nullable=True)
    lastname = Column(String(length=255))
    hashed_password = Column(String(length=255))
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    last_login = Column(DateTime, nullable=True)
    owned_courses = relationship("Course", back_populates="owner")
    courses = relationship("Course", secondary="coursemembers", back_populates="members")
