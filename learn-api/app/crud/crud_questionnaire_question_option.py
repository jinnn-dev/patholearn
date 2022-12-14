from app.crud.base import CRUDBase

from app.models.questionnaire_question_option import QuestionnaireQuestionOption
from app.schemas.questionnaire_question_option import (
    QuestionnaireQuestionOptionUpdate,
    QuestionnaireQuestionOptionCreate,
)


class CRUDQuestionnaireQuestionOption(
    CRUDBase[
        QuestionnaireQuestionOption,
        QuestionnaireQuestionOptionCreate,
        QuestionnaireQuestionOptionUpdate,
    ]
):
    pass


crud_questionnaire_question_option = CRUDQuestionnaireQuestionOption(
    QuestionnaireQuestionOption
)
