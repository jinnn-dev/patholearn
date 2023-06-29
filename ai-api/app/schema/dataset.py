import datetime
from typing import Dict, Literal, Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field
from app.schema.py_object_id import PyObjectId
from app.schema.base_mongo_model import BaseMongoModel

DatasetType = Literal["classification", "detection", "segmentation"]
DatasetStatus = Literal["saving", "processing", "completed", "failed"]


class DatasetDimension(BaseModel):
    x: int
    y: int


class DatasetMetadata(BaseModel):
    class_map: Optional[Dict]
    classes: Optional[List]
    is_grayscale: Optional[bool]
    dimension: Optional[DatasetDimension]


class Dataset(BaseMongoModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    creator_id: str = Field(...)
    name: str = Field(...)
    description: Optional[str] = None
    dataset_type: DatasetType = Field(default="Classification")
    created_at: datetime.datetime = Field(...)
    status: Optional[DatasetStatus]
    clearml_dataset: Optional[Dict]
    metadata: Optional[DatasetMetadata]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "9a201441-0d82-4d65-bd38-b2f14b700803",
                "name": "Test",
                "description": "That is a test project",
                "dataset_type": "Classification",
                "created_at": "2023-06-08T19:15:10.029+00:00",
                "status": "saving",
            }
        }
