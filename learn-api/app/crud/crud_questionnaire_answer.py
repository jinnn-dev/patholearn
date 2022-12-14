from app.crud.base import CRUDBase

from app.models.questionnaire_answer import QuestionnaireAnswer
from app.schemas.questionnaire_answer import (
    QuestionnaireAnswerCreate,
    QuestionnaireAnswerUpdate,
)


class CRUDQuestionnaireAnswer(
    CRUDBase[QuestionnaireAnswer, QuestionnaireAnswerCreate, QuestionnaireAnswerUpdate]
):
    pass


crud_questionnaire_answer = CRUDQuestionnaireAnswer(QuestionnaireAnswer)
