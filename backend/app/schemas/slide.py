from typing import Optional

from pydantic.main import BaseModel


class Slide(BaseModel):
    name: str
    file_id: str
    status: str
    mag: Optional[int]
    width: Optional[int]
    height: Optional[int]
    mpp: Optional[float]

    class Config:
        orm_mode = True


class SlideUpdate(Slide):
    file_id: str
    name: Optional[str]
    status: Optional[str]
    mag: Optional[int]
    width: Optional[int]
    height: Optional[int]
    mpp: Optional[float]


class SlideCreate(Slide):
    name: str
    file_id: str
    status: str
