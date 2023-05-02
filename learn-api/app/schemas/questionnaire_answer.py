from pydantic import BaseModel
from typing import Optional


class QuestionnaireAnswerBase(BaseModel):
    answer: Optional[str]
    selected: Optional[str]
    question_option_id: Optional[int]
    questionnaire_id: Optional[int]


class QuestionnaireAnswerCreate(QuestionnaireAnswerBase):
    user_id: Optional[str]
    question_id: int
    question_option_id: Optional[int]


class QuestionnaireAnswerUpdate(QuestionnaireAnswerBase):
    id: int
    user_id: Optional[str]
    question_id: Optional[int]


class QuestionnaireAnswerInDBBase(QuestionnaireAnswerBase):
    id: int
    user_id: str
    question_id: int

    class Config:
        orm_mode = True


class QuestionnaireAnswerInDB(QuestionnaireAnswerInDBBase):
    pass


class QuestionnaireAnswer(QuestionnaireAnswerInDB):
    pass
