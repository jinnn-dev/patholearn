import logging
import os
from enum import IntEnum
from typing import Dict, Optional

from app.db.pydantic_objectid import PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import MongoClient


class SlideStatus(IntEnum):
    ERROR = 0
    SUCCESS = 1
    RUNNING = 2


class SlideSchema(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias='_id')
    name: str
    slide_id: str
    status: SlideStatus
    metadata: Optional[Dict]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class CreateSlide(BaseModel):
    name: str
    slide_id: str
    status: SlideStatus
    metadata: Optional[Dict]


class UpdateSlide(BaseModel):
    name: Optional[str]
    status: Optional[SlideStatus]
    metadata: Optional[Dict]


class SlideDatabase:

    def __init__(self):
        self.connection_url = os.getenv("DATABASE_URL")
        if self.connection_url:
            self.client = MongoClient(os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=5000)
            self.db = self.client["slidedb"]
            self.collection = self.db["slides"]
        else:
            print("No connection_url available")
        self.connection_is_healthy()

    def init_client(self):
        self.connection_url = os.getenv("DATABASE_URL")
        if self.connection_url:
            self.client = MongoClient(os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=5000)
            self.db = self.client["slidedb"]
            self.collection = self.db["slides"]
        else:
            print("No connection_url available")

    def connection_is_healthy(self) -> bool:
        try:
            print(self.client.server_info())
            return True
        except Exception as e:
            print("Unable to connect to MongoDB server:")
            print(e)
            return False

    def insert_slide(self, slide: SlideSchema) -> ObjectId:
        logging.info(slide.dict(skip_defaults=True))
        try:
            return self.collection.insert_one(slide.dict(skip_defaults=True))
        except Exception as e:
            print("Slide could not be inserted")
            print(e)

    def update_slide(self, slide_update: UpdateSlide, slide_id: str):
        slide_query = {"slide_id": slide_id}
        logging.info(slide_update.dict(skip_defaults=True))
        values_to_update = {"$set": slide_update.dict(skip_defaults=True)}
        return self.collection.update_one(slide_query, values_to_update)

    def get_all_slides(self):
        return self.collection.find({}, {'_id': False})

    def slide_with_name_exists(self, name: str) -> bool:
        return self.collection.count_documents({ 'name': name }, limit = 1) != 0

slide_db = SlideDatabase()
