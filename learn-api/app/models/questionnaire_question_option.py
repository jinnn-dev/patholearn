from sqlalchemy import Integer, Column, ForeignKey, String

from app.db import Base


class QuestionnaireQuestionOption(Base):
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questionnairequestion.id"))
    order = Column(Integer, nullable=False, unique=True)
    value = Column(String(length=255), nullable=False)
    