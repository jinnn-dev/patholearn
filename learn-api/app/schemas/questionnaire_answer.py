from pydantic import BaseModel
from typing import Optional


class QuestionnaireAnswerBase(BaseModel):
    answer: Optional[str]


class QuestionnaireAnswerCreate(QuestionnaireAnswerBase):
    user_id: int
    question_id: int


class QuestionnaireAnswerUpdate(QuestionnaireAnswerBase):
    id: int
    user_id: Optional[int]
    question_id: Optional[int]


class QuestionnaireAnswerInDBBase(QuestionnaireAnswerBase):
    id: int
    user_id: int
    question_id: int

    class Config:
        orm_mode: True


class QuestionnaireAnswerInDB(QuestionnaireAnswerInDBBase):
    pass


class QuestionnaireAnswer(QuestionnaireAnswerInDB):
    pass
