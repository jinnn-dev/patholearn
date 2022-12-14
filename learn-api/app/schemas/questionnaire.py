from pydantic import BaseModel

from typing import Optional, List

from app.schemas.questionnaire_question import QuestionnaireQuestion


class QuestionnaireBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    is_mandatory: bool = False
    questions: Optional[List[QuestionnaireQuestion]]
    is_before: Optional[bool]


class QuestionnaireCreate(QuestionnaireBase):
    pass


class QuestionnaireUpdate(QuestionnaireBase):
    id: int
    is_mandatory: Optional[bool]


class QuestionnaireInDBBase(QuestionnaireBase):
    id: int

    class Config:
        orm_mode: True


class QuestionnaireInDB(QuestionnaireInDBBase):
    pass


class Questionnaire(QuestionnaireBase):
    pass
