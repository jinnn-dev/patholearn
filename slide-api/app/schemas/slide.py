from enum import IntEnum
from typing import Dict, List, Optional

from app.db.pydantic_objectid import PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field


class SlideStatus(IntEnum):
    ERROR = 0
    SUCCESS = 1
    RUNNING = 2


class Slide(BaseModel):
    name: str
    slide_id: str
    status: SlideStatus
    metadata: Optional[Dict]
    children: Optional[List[str]]


class DatabaseSlide(Slide):
    id: Optional[PydanticObjectId] = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class DatabaseSlideNoMetadata(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    name: str
    slide_id: str
    status: SlideStatus

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


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
    slide_id: Optional[str]
    name: Optional[str]
    status: Optional[SlideStatus]
    metadata: Optional[Dict]
    children: Optional[List[str]]
