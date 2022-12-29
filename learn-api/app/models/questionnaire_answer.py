from sqlalchemy import Column, Integer, Text, ForeignKey, String

from app.db.base_class import Base


class QuestionnaireAnswer(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    questionnaire_id = Column(Integer, ForeignKey("questionnaire.id"))
    question_id = Column(Integer, ForeignKey("questionnairequestion.id"))
    question_option_id = Column(Integer, ForeignKey("questionnairequestionoption.id"))
    selected = Column(String(500))
    answer = Column(Text, nullable=True)
