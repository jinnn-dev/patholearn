from typing import Optional

from pydantic import BaseModel

from app.schemas.questionnaire_question_option import QuestionnaireQuestionOption
from app.schemas.user import User


class QuestionnaireAnswerStatistic(BaseModel):
    id: Optional[int]
    answer: Optional[str]
    selected: Optional[str]
    question_option: Optional[QuestionnaireQuestionOption]
    user: Optional[User]
    questionnaire_id: Optional[int]