from app.crud.base import CRUDBase
from app.models.questionnaire import Questionnaire
from app.models.task_questionnaires import TaskQuestionnaires
from app.schemas.questionnaire import QuestionnaireCreate, QuestionnaireUpdate
from sqlalchemy.orm import Session


class CRUDQuestionnaire(
    CRUDBase[Questionnaire, QuestionnaireCreate, QuestionnaireUpdate]
):
    def add_questionnaire_to_task(
        self, db: Session, *, task_id: int, questionnaire_id: int
    ):
        exists = db.query(TaskQuestionnaires).filter(
            TaskQuestionnaires.task_id == task_id,
            TaskQuestionnaires.questionnaire_id == questionnaire_id,
        )
        if exists:
            return None

        db_obj = TaskQuestionnaires()
        db_obj.task_id = task_id
        db_obj.questionnaire_id = questionnaire_id
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_questionnaire = CRUDQuestionnaire(Questionnaire)
