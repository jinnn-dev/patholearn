from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.crud.crud_questionnaire import crud_questionnaire
from app.crud.crud_questionnaire_answer import crud_questionnaire_answer
from app.crud.crud_questionnaire_question import crud_questionnaire_question
from app.crud.crud_questionnaire_question_option import (
    crud_questionnaire_question_option,
)
from app.crud.crud_task import crud_task
from app.schemas.questionnaire import (
    Questionnaire,
    QuestionnaireCreate,
    QuestionnaireUpdate,
)
from app.schemas.questionnaire_answer import QuestionnaireAnswerCreate
from app.api.deps import (
    get_db,
    get_current_active_superuser,
    get_current_user,
    check_if_user_can_access_task,
)
from pydantic import BaseModel, parse_obj_as
from sqlalchemy.orm import Session

from app.schemas.questionnaire_question import QuestionnaireQuestionCreate
from app.schemas.questionnaire_question_option import QuestionnaireQuestionOptionCreate
from app.schemas.user import User

router = APIRouter()


class PostSchema(QuestionnaireCreate):
    is_before: Optional[bool]


@router.post("/answers/multiple")
def save_questionnaires_answers(
    *,
    db: Session = Depends(get_db),
    answers: List[QuestionnaireAnswerCreate],
    current_user: User = Depends(get_current_user),
):
    answers_db = []
    for answer in answers:
        answer.user_id = current_user.id
        answer_db = crud_questionnaire_answer.create(db, obj_in=answer)
        answers_db.append(answer_db)
    return answers_db


@router.post("/{task_id}")
def create_questionnaire_to_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    questionnaire: PostSchema,
    current_user: User = Depends(get_current_active_superuser),
):
    questionnaire_create = QuestionnaireCreate()
    questionnaire_create.is_mandatory = questionnaire.is_mandatory
    questionnaire_create.name = questionnaire.name
    questionnaire_create.questions = []

    questionnaire_create.description = questionnaire.description
    questionnaire_db = crud_questionnaire.create(db, obj_in=questionnaire_create)
    questions = questionnaire.questions
    for question in questions:

        question_create = QuestionnaireQuestionCreate(
            order=question.order,
            question_type=question.question_type,
            question_text=question.question_text,
            questionnaire_id=questionnaire_db.id,
        )
        question_create.answers = []
        question_create.options = []
        # question_create.questionnaire_id = questionnaire_db.id
        # question_create.question_text = question.question_text
        # question_create.question_type = question.question_type
        # question_create.order = question.order
        question_create.is_mandatory = question.is_mandatory
        question_db = crud_questionnaire_question.create(db, obj_in=question_create)

        for option in question.options:
            option_create = QuestionnaireQuestionOptionCreate(
                question_id=question_db.id,
                order=option.order,
                value=option.value,
                with_input=option.with_input,
            )
            print(type(bool(option.with_input)))
            # option_create.question_id = question_db
            # option_create.order = option.order
            # option_create.value = option.value
            # option_create.with_input = option.with_input
            crud_questionnaire_question_option.create(db, obj_in=option_create)

    crud_questionnaire.add_questionnaire_to_task(
        db,
        task_id=task_id,
        questionnaire_id=questionnaire_db.id,
        is_before=questionnaire.is_before,
    )

    return questionnaire_db


@router.post("", response_model=Questionnaire)
def create_questionnaire(
    *,
    db: Session = Depends(get_db),
    questionnaire_create: Any,
    current_user: User = Depends(get_current_active_superuser),
):
    questionnaire = crud_questionnaire.create(db=db, obj_in=questionnaire_create)

    return questionnaire


@router.put("", response_model=Questionnaire)
def update_questionnaire(
    *,
    db: Session = Depends(get_db),
    questionnaire_update: QuestionnaireUpdate,
    current_user: User = Depends(get_current_active_superuser),
):
    questionnaire_db = crud_questionnaire.get(db, id=questionnaire_update.id)
    questionnaire = crud_questionnaire.update(
        db, obj_in=questionnaire_update, db_obj=questionnaire_db
    )
    return questionnaire


@router.get("/{task_id}", response_model=Any)
def get_questionnaires(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user=Depends(get_current_user),
):
    questionnaires = crud_questionnaire.get_questionnaires_to_task(
        db, task_id=task_id, user_id=current_user.id
    )
    return questionnaires
