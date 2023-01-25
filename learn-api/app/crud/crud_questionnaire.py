from app.crud.base import CRUDBase
from app.crud.crud_questionnaire_answer import crud_questionnaire_answer
from app.models.questionnaire import Questionnaire
from app.models.questionnaire_answer import QuestionnaireAnswer
from app.models.task_questionnaires import TaskQuestionnaires
from app.schemas.questionnaire import (
    QuestionnaireCreate,
    QuestionnaireUpdate,
    QuestionnaireDetail,
)
from sqlalchemy.orm import Session

from app.utils.logger import logger


class CRUDQuestionnaire(
    CRUDBase[Questionnaire, QuestionnaireCreate, QuestionnaireUpdate]
):
    def add_questionnaire_to_task(
        self, db: Session, *, task_id: int, questionnaire_id: int, is_before: bool
    ):
        db_obj = TaskQuestionnaires()
        db_obj.task_id = task_id
        db_obj.questionnaire_id = questionnaire_id
        db_obj.is_before = is_before
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_questionnaires_to_task(
        self, db: Session, *, task_id: int, user_id: int, is_before: bool = None
    ):
        if is_before is None:
            task_questionnaires = (
                db.query(TaskQuestionnaires)
                .filter(TaskQuestionnaires.task_id == task_id)
                .all()
            )
        else:
            task_questionnaires = (
                db.query(TaskQuestionnaires)
                .filter(TaskQuestionnaires.task_id == task_id)
                .filter(TaskQuestionnaires.is_before == is_before)
                .all()
            )
        questionnaires = []
        questions = []
        for questionnaire in task_questionnaires:
            questionnaire_db = crud_questionnaire.get(
                db, id=questionnaire.questionnaire_id
            )
            schema = QuestionnaireDetail(
                id=questionnaire_db.id,
                name=questionnaire_db.name,
                description=questionnaire_db.description,
                is_mandatory=questionnaire_db.is_mandatory,
                questions=questionnaire_db.questions,
                is_before=questionnaire.is_before,
            )

            questionnaires.append(schema)
        return questionnaires

    def is_before(self, db: Session, *, questionnaire_id: int, task_id: int) -> bool:
        result =  db.query(TaskQuestionnaires.is_before).filter(TaskQuestionnaires.task_id == task_id).filter(TaskQuestionnaires.questionnaire_id == questionnaire_id).first()
        return result[0]

crud_questionnaire = CRUDQuestionnaire(Questionnaire)
