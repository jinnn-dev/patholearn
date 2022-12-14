from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.crud.crud_questionnaire import crud_questionnaire
from app.crud.crud_task import crud_task
from app.schemas.questionnaire import (
    Questionnaire,
    QuestionnaireCreate,
    QuestionnaireUpdate,
)
from app.api.deps import (
    get_db,
    get_current_active_superuser,
    check_if_user_can_access_task,
)

from sqlalchemy.orm import Session

from app.schemas.user import User

router = APIRouter()


@router.post("", response_model=Questionnaire)
def create_questionnaire(
    *,
    db: Session = Depends(get_db),
    questionnaire_create: QuestionnaireCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    questionnaire = crud_questionnaire.create(db=db, obj_in=questionnaire_create)

    return questionnaire


@router.put("", response_model=Questionnaire)
def update_questionnaire(
    *,
    db: Session = Depends(get_db),
    questionnaire_update: QuestionnaireUpdate,
    current_user: User = Depends(get_current_active_superuser)
):
    questionnaire_db = crud_questionnaire.get(db, id=questionnaire_update.id)
    questionnaire = crud_questionnaire.update(
        db, obj_in=questionnaire_update, db_obj=questionnaire_db
    )
    return questionnaire
