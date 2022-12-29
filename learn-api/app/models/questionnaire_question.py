from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class QuestionnaireQuestion(Base):
    id = Column(Integer, primary_key=True, index=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaire.id"))
    order = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    is_mandatory = Column(Boolean, default=False)
    question_type = Column(Integer, nullable=False)
    answers = relationship("QuestionnaireAnswer", cascade="all, delete-orphan")
    options = relationship(
        "QuestionnaireQuestionOption",
        cascade="all, delete-orphan",
        order_by="QuestionnaireQuestionOption.order",
    )
