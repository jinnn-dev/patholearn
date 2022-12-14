from pydantic import BaseModel

from typing import Optional


class QuestionnaireQuestionOptionBase(BaseModel):
    order: int
    value: str
    with_input: bool


class QuestionnaireQuestionOptionCreate(QuestionnaireQuestionOptionBase):
    question_id: Optional[int]


class QuestionnaireQuestionOptionUpdate(QuestionnaireQuestionOptionBase):
    order: Optional[int]
    value: Optional[str]


class QuestionnaireQuestionOptionInDBBase(QuestionnaireQuestionOptionBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True


class QuestionnaireQuestionOptionInDB(QuestionnaireQuestionOptionInDBBase):
    pass


class QuestionnaireQuestionOption(QuestionnaireQuestionOptionInDB):
    pass
