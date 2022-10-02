from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class CourseMembers(Base):
    course_id = Column(Integer, ForeignKey("course.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
