from sqlalchemy import asc

from app.crud.base import CRUDBase
from sqlalchemy.orm import Session

from app.models.questionnaire_answer import QuestionnaireAnswer
from app.models.questionnaire_question_option import QuestionnaireQuestionOption
from app.models.user import User
from app.schemas.questionnaire_answer import (
    QuestionnaireAnswerCreate,
    QuestionnaireAnswerUpdate,
)
from app.utils.logger import logger


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

    def check_if_answers_exists(self, db: Session, *, questionnaire_id: int):
        exists_stmt = (
            db.query(self.model)
            .filter(self.model.questionnaire_id == questionnaire_id)
            .exists()
        )
        exists = db.query(exists_stmt).scalar()
        return exists

    def get_answers_to_questionnaire(self, db: Session, *, questionnaire_id):
        answers = (
            db.query(self.model, User, QuestionnaireQuestionOption)
            .filter(self.model.questionnaire_id == questionnaire_id)
            .order_by(asc(self.model.selected))
            .join(User, self.model.user_id == User.id)
            .join(
                QuestionnaireQuestionOption,
                self.model.question_option_id == QuestionnaireQuestionOption.id,
            )
            .all()
        )
        return answers


crud_questionnaire_answer = CRUDQuestionnaireAnswer(QuestionnaireAnswer)
