from app.crud.base import CRUDBase

from app.models.questionnaire_question import QuestionnaireQuestion
from app.schemas.questionnaire_question import (
    QuestionnaireQuestionCreate,
    QuestionnaireQuestionUpdate,
)


class CRUDQuestionnaireQuestion(
    CRUDBase[
        QuestionnaireQuestion, QuestionnaireQuestionCreate, QuestionnaireQuestionUpdate
    ]
):
    pass


crud_questionnaire_question = CRUDQuestionnaireQuestion(QuestionnaireQuestion)
