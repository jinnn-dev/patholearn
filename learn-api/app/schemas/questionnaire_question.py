from enum import IntEnum
from pydantic import BaseModel
from typing import List, Optional

from app.schemas.questionnaire_answer import QuestionnaireAnswer
from app.schemas.questionnaire_question_option import (
    QuestionnaireQuestionOption,
    QuestionnaireQuestionOptionCreate,
)


class QuestionnaireQuestionType(IntEnum):
    SINGLE_CHOICE = 0
    FREE_TEXT = 1


class QuestionnaireQuestionBase(BaseModel):
    order: int
    question_text: str
    is_mandatory: bool = False
    question_type: QuestionnaireQuestionType
    answers: Optional[List[QuestionnaireAnswer]]
    options: Optional[List[QuestionnaireQuestionOption]]


class QuestionnaireQuestionCreate(QuestionnaireQuestionBase):
    questionnaire_id: Optional[int]
    options: Optional[List[QuestionnaireQuestionOptionCreate]]


class QuestionnaireQuestionUpdate(QuestionnaireQuestionBase):
    id: int
    questionnaire_id: Optional[int]
    order: Optional[int]
    question_text: Optional[str]
    question_type: Optional[QuestionnaireQuestionType]
    answers: Optional[List[QuestionnaireAnswer]]
    options: Optional[List[QuestionnaireQuestionOption]]


class QuestionnaireQuestionInDBBase(QuestionnaireQuestionBase):
    id: int
    questionnaire_id: int

    class Config:
        orm_mode = True


class QuestionnaireQuestionInDB(QuestionnaireQuestionInDBBase):
    pass


class QuestionnaireQuestion(QuestionnaireQuestionInDB):
    pass
