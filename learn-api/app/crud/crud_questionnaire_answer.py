from app.crud.base import CRUDBase
from sqlalchemy.orm import Session

from app.models.questionnaire_answer import QuestionnaireAnswer
from app.schemas.questionnaire_answer import (
    QuestionnaireAnswerCreate,
    QuestionnaireAnswerUpdate,
)


class CRUDQuestionnaireAnswer(
    CRUDBase[QuestionnaireAnswer, QuestionnaireAnswerCreate, QuestionnaireAnswerUpdate]
):
    def remove_to_questionnaire(self, db: Session, *, questionnaire_id: int):
        questionnaires = (
            db.query(self.model)
            .filter(self.model.questionnaire_id == questionnaire_id)
            .all()
        )
        for questionnaire in questionnaires:
            crud_questionnaire_answer.remove(db, model_id=questionnaire.id)


crud_questionnaire_answer = CRUDQuestionnaireAnswer(QuestionnaireAnswer)
