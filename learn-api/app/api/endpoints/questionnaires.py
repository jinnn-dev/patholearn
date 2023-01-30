from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pip._internal.network.utils import response_chunks
from starlette.responses import StreamingResponse

from app.core.export.questionnaire_exporter import (
    QuestionnaireRow,
    QuestionnaireExporter,
)
from app.crud.crud_questionnaire import crud_questionnaire
from app.crud.crud_questionnaire_answer import crud_questionnaire_answer
from app.crud.crud_questionnaire_question import crud_questionnaire_question
from app.crud.crud_questionnaire_question_option import (
    crud_questionnaire_question_option,
)
from app.crud.crud_task import crud_task
from app.models.task_questionnaires import TaskQuestionnaires
from app.schemas.questionnaire import (
    Questionnaire,
    QuestionnaireCreate,
    QuestionnaireUpdate,
    QuestionnaireInDB,
)
from app.schemas.questionnaire_answer import (
    QuestionnaireAnswerCreate,
    QuestionnaireAnswer,
)
from app.api.deps import (
    get_db,
    get_current_active_superuser,
    get_current_user,
    check_if_user_can_access_task,
)
from pydantic import BaseModel, parse_obj_as
from sqlalchemy.orm import Session

from app.schemas.questionnaire_answer_statistic import QuestionnaireAnswerStatistic
from app.schemas.questionnaire_question import (
    QuestionnaireQuestionCreate,
    QuestionnaireQuestionUpdate,
)
from app.schemas.questionnaire_question_option import (
    QuestionnaireQuestionOptionCreate,
    QuestionnaireQuestionOption,
)
from app.schemas.user import User
from app.utils.logger import logger

router = APIRouter()


class PostSchema(QuestionnaireCreate):
    is_before: Optional[bool]


@router.get(
    "/{questionnaire_id}/statistic", response_model=List[QuestionnaireAnswerStatistic]
)
def get_questionnaire_statistic(
    *,
    db: Session = Depends(get_db),
    questionnaire_id,
    current_user=Depends(get_current_active_superuser),
):

    db_answers = crud_questionnaire_answer.get_answers_to_questionnaire(
        db, questionnaire_id=questionnaire_id
    )
    result = []
    for answer in db_answers:
        db_answer = answer[0]
        user = answer[1]
        option = answer[2]
        statistic = QuestionnaireAnswerStatistic()
        statistic.id = db_answer.id
        statistic.selected = db_answer.selected
        statistic.answer = db_answer.answer
        statistic.questionnaire_id = db_answer.questionnaire_id
        statistic.user = parse_obj_as(User, user)
        statistic.question_option = parse_obj_as(QuestionnaireQuestionOption, option)
        result.append(statistic)
    return result


@router.get("/{questionnaire_id}/statistic/download")
def download_questionnaire_statistic(
    *,
    db: Session = Depends(get_db),
    questionnaire_id: int,
    current_user=Depends(get_current_active_superuser),
):
    export_data = crud_questionnaire.get_questionnaire_export(
        db, questionnaire_id=questionnaire_id
    )
    result = []
    for data in export_data:
        item = QuestionnaireRow(
            question_text=data[0],
            firstname=data[1],
            middlename=data[2],
            lastname=data[3],
            selection=data[4],
            answer=data[5],
        )
        result.append(item)

    output = QuestionnaireExporter.export_questionnaire_answers(db, result)

    headers = {
        "Content-Disposition": 'attachment; filename="' + str(questionnaire_id) + '"'
    }

    return StreamingResponse(output, headers=headers)


@router.post("/answers/multiple", response_model=List[QuestionnaireAnswer])
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


@router.post("/{task_id}", response_model=QuestionnaireInDB)
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
    delattr(questionnaire_create, "is_before")
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
        question_create.is_mandatory = question.is_mandatory
        question_db = crud_questionnaire_question.create(db, obj_in=question_create)

        for option in question.options:
            option_create = QuestionnaireQuestionOptionCreate(
                question_id=question_db.id,
                order=option.order,
                value=option.value,
                with_input=option.with_input,
            )
            crud_questionnaire_question_option.create(db, obj_in=option_create)

    crud_questionnaire.add_questionnaire_to_task(
        db,
        task_id=task_id,
        questionnaire_id=questionnaire_db.id,
        is_before=questionnaire.is_before,
    )
    return questionnaire_db


@router.put("", response_model=QuestionnaireInDB)
def update_questionnaire(
    *,
    db: Session = Depends(get_db),
    questionnaire_update: QuestionnaireUpdate,
    current_user: User = Depends(get_current_active_superuser),
):
    questionnaire = crud_questionnaire.get(db, id=questionnaire_update.id)
    crud_questionnaire.update(db, db_obj=questionnaire, obj_in=questionnaire_update)

    for question in questionnaire_update.questions:
        if question.id is None:
            logger.debug("ID is none")
            question_create = QuestionnaireQuestionCreate(
                order=question.order,
                question_type=question.question_type,
                question_text=question.question_text,
                questionnaire_id=questionnaire.id,
            )
            question_create.answers = []
            question_create.options = []
            question_create.is_mandatory = question.is_mandatory
            question_db = crud_questionnaire_question.create(db, obj_in=question_create)
            for option in question.options:
                option_create = QuestionnaireQuestionOptionCreate(
                    question_id=question_db.id,
                    order=option.order,
                    value=option.value,
                    with_input=option.with_input,
                )
                crud_questionnaire_question_option.create(db, obj_in=option_create)
        else:
            db_question = crud_questionnaire_question.get(db, id=question.id)
            question_update = QuestionnaireQuestionUpdate(id=question.id)
            question_update.question_text = question.question_text
            question_update.is_mandatory = question.is_mandatory
            crud_questionnaire_question.update(
                db, db_obj=db_question, obj_in=question_update
            )

    updated_questionnaire = crud_questionnaire.get(db, id=questionnaire_update.id)

    return updated_questionnaire


@router.get("/{questionnaire_id}/answers/exists", response_model=bool)
def check_if_questionnaire_answers_exists(
    *,
    db: Session = Depends(get_db),
    questionnaire_id: int,
    current_user: User = Depends(get_current_active_superuser),
):
    exists = crud_questionnaire_answer.check_if_answers_exists(
        db, questionnaire_id=questionnaire_id
    )
    return exists


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


@router.delete("/{questionnaire_id}")
def delete_questionnaire(
    *,
    db: Session = Depends(get_db),
    questionnaire_id: int,
    current_user: User = Depends(get_current_active_superuser),
):
    crud_questionnaire.remove(db, model_id=questionnaire_id)


@router.get("/{task_id}", response_model=Any)
def get_questionnaires(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    is_before: bool = None,
    current_user=Depends(get_current_user),
):
    questionnaires = crud_questionnaire.get_questionnaires_to_task(
        db, task_id=task_id, user_id=current_user.id, is_before=is_before
    )
    return questionnaires
