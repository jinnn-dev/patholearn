from sqlalchemy import Column, Integer, Text, ForeignKey

from app.db.base_class import Base


class QuestionnaireAnswer(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    question_id = Column(Integer, ForeignKey("questionnairequestion.id"))
    answer = Column(Text, nullable=True)
