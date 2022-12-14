from sqlalchemy import Column, Integer, Text, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Questionnaire(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    is_mandatory = Column(Boolean, default=False)
    questions = relationship(
        "QuestionnaireQuestion",
        cascade="all, delete-orphan",
        order_by="QuestionnaireQuestion.order",
    )
    tasks = relationship(
        "Task",
        secondary="taskquestionnaires",
        back_populates="questionnaires",
    )
