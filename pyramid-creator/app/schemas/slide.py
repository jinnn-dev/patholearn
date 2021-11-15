from enum import IntEnum
from typing import Optional, Dict

from bson import ObjectId
from pydantic import BaseModel, Field

from app.db.pydantic_objectid import PydanticObjectId


class SlideStatus(IntEnum):
    ERROR = 0
    SUCCESS = 1
    RUNNING = 2


class Slide(BaseModel):
    name: str
    slide_id: str
    status: SlideStatus
    metadata: Optional[Dict]


class DatabaseSlide(Slide):
    id: Optional[PydanticObjectId] = Field(alias='_id')

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class DatabaseSlideNoMetadata(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias='_id')
    name: str
    slide_id: str
    status: SlideStatus

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class SlideNoMetadata(BaseModel):
    name: str
    slide_id: str
    status: SlideStatus


class CreateSlide(BaseModel):
    name: str
    slide_id: str
    status: SlideStatus
    metadata: Optional[Dict]


class UpdateSlide(BaseModel):
    name: Optional[str]
    status: Optional[SlideStatus]
    metadata: Optional[Dict]
