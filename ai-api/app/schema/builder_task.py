from typing import Optional
from bson import ObjectId
from app.schema.py_object_id import PyObjectId

from pydantic import BaseModel, Field


class CreateBuilderTask(BaseModel):
    name: str
    project_id: str


class BuilderTask(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    user_id: str = Field(...)
    project_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "ObjectId",
                "name": "Task",
                "user_id": "8c29bcc1-2cb8-4c8d-93bc-42aa84e2b3a2",
                "project_id": "a84565dbf2524b1faf4129bfcf53418b",
            }
        }
