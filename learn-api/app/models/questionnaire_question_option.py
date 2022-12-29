from sqlalchemy import Integer, Column, ForeignKey, String, Boolean

from app.db import Base


class QuestionnaireQuestionOption(Base):
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questionnairequestion.id"))
    order = Column(Integer, nullable=False)
    value = Column(String(length=255), nullable=False)
    with_input = Column(Boolean(), default=False)
