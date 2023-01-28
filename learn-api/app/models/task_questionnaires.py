from sqlalchemy import Integer, Column, ForeignKey, Boolean
from app.db.base_class import Base


class TaskQuestionnaires(Base):
    task_id = Column(
        Integer, ForeignKey("task.id", ondelete="CASCADE"), primary_key=True
    )
    questionnaire_id = Column(
        Integer, ForeignKey("questionnaire.id", ondelete="CASCADE"), primary_key=True
    )
    is_before = Column(Boolean, nullable=False)
