from typing import List, Optional
from app.schema.task import TaskNoGraph
from bson import ObjectId
from pydantic import BaseModel, Field
from app.schema.py_object_id import PyObjectId
from app.schema.base_mongo_model import BaseMongoModel
import datetime


class Project(BaseMongoModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    name: str = Field(...)
    description: Optional[str] = None
    created_at: datetime.datetime = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "9a201441-0d82-4d65-bd38-b2f14b700803",
                "name": "Test",
                "description": "That is a test project",
                "created_at": "2023-06-08T19:15:10.029+00:00",
            }
        }


class ProjectWithTasks(BaseModel):
    project: Project
    tasks: List[TaskNoGraph]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CreateProject(BaseModel):
    name: str = Field(...)
    description: Optional[str] = None


class UpdateProject(BaseModel):
    id: str
    name: str = Field(...)
    description: Optional[str] = None
