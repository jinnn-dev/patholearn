from pydantic import BaseModel

from typing import Optional


class QuestionnaireQuestionOptionBase(BaseModel):
    order: int
    value: str


class QuestionnaireQuestionOptionCreate(QuestionnaireQuestionOptionBase):
    question_id: int


class QuestionnaireQuestionOptionUpdate(QuestionnaireQuestionOptionBase):
    order: Optional[int]
    value: Optional[str]


class QuestionnaireQuestionOptionInDBBase(QuestionnaireQuestionOptionBase):
    id: int
    question_id: int

    class Config:
        orm_mode: True


class QuestionnaireQuestionOptionInDB(QuestionnaireQuestionOptionInDBBase):
    pass


class QuestionnaireQuestionOption(QuestionnaireQuestionOptionInDB):
    pass
