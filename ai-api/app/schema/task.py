from datetime import datetime
from typing import List, Optional
from app.schema.base_mongo_model import BaseMongoModel

from bson import ObjectId
from app.schema.py_object_id import PyObjectId
from pydantic import BaseModel, Field


class BuilderState(BaseModel):
    nodes: List[dict] = Field(...)
    connections: List[dict] = Field(...)
    positions: List[dict] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "nodes": [],
                "connections": [],
                "positions": [],
            }
        }


class TaskVersion(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    builder: BuilderState = Field(...)
    clearml_id: Optional[str] = None
    creation_date: datetime = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "9a201441-0d63-4d65-bd38-b2f14b700803",
                "builder": {},
                "clearml_id": None,
            }
        }


class TaskVersionNoBuilder(TaskVersion):
    builder: Optional[BuilderState] = None


class UpdateTaskVersion(BaseModel):
    id: PyObjectId
    builder: Optional[BuilderState]


class Task(BaseMongoModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    creator_id: str = Field(...)
    project_id: str = Field(...)
    creation_date: datetime = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(...)
    versions: List[TaskVersion] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "9a201441-0d63-4d65-bd38-b2f14b700803",
                "creator_id": "740f0751-eb93-414c-b5e0-5e2caa5cfcb2",
                "project_id": "8134ccd1e5f04ac4b2cf9a64e48e7907",
                "creation_date": "",
                "name": "Test",
                "description": "This is a description",
                "versions": [],
            }
        }


class TaskNoBuilder(Task):
    versions: List[TaskVersionNoBuilder]


class CreateTask(BaseModel):
    name: str
    description: Optional[str]
    project_id: str
