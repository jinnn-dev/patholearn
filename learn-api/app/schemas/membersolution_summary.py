from typing import List, Optional

from pydantic import BaseModel


class SummaryUser(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]


class SummaryRow(BaseModel):
    user: Optional[SummaryUser]
    summary: Optional[List[int]]


class MembersolutionSummary(BaseModel):
    tasks: Optional[List[str]]
    rows: Optional[List[SummaryRow]]
