# import logging
# import os
# from enum import IntEnum
# from typing import Dict, List, Optional
#
# from bson import ObjectId
# from pydantic import BaseModel, Field, parse_obj_as
# from pymongo import MongoClient
# from pymongo.results import DeleteResult, UpdateResult
#
# from app.db.pydantic_objectid import PydanticObjectId
#
#
# class SlideStatus(IntEnum):
#     ERROR = 0
#     SUCCESS = 1
#     RUNNING = 2
#
#
# class Slide(BaseModel):
#     name: str
#     slide_id: str
#     status: SlideStatus
#     metadata: Optional[Dict]
#
#
# class DatabaseSlide(Slide):
#     id: Optional[PydanticObjectId] = Field(alias='_id')
#
#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {
#             ObjectId: str
#         }
#
#
# class DatabaseSlideNoMetadata(BaseModel):
#     id: Optional[PydanticObjectId] = Field(alias='_id')
#     name: str
#     slide_id: str
#     status: SlideStatus
#
#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {
#             ObjectId: str
#         }
#
#
# class SlideNoMetadata(BaseModel):
#     name: str
#     slide_id: str
#     status: SlideStatus
#
#
# class CreateSlide(BaseModel):
#     name: str
#     slide_id: str
#     status: SlideStatus
#     metadata: Optional[Dict]
#
#
# class UpdateSlide(BaseModel):
#     name: Optional[str]
#     status: Optional[SlideStatus]
#     metadata: Optional[Dict]
#
#
# class SlideDatabase:
#     """
#     Class which offers methods for CRUD Operation on slide entries in the MongoDB
#     """
#
#     def __init__(self):
#         self.connection_url = os.getenv("DATABASE_URL")
#         if self.connection_url:
#             self.client = MongoClient(os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=5000)
#             self.db = self.client["slidedb"]
#             self.collection = self.db["slides"]
#         else:
#             print("No connection_url available")
#         self.connection_is_healthy()
#
#     def connection_is_healthy(self) -> bool:
#         """
#         Checks whether the connection to the MongoDB server is healthy or not
#
#         :return: If the connection is healthy or not
#         """
#         try:
#             self.client.server_info()
#             return True
#         except Exception as e:
#             print("Unable to connect to MongoDB server:")
#             print(e)
#             return False
#
#     def insert_slide(self, slide: Slide) -> ObjectId:
#         """
#         Inserts a new slide record into the database
#
#         :param slide: The slide to insert
#         :return: The internal ObjectId of the database slide entry
#         """
#         logging.info(slide.dict(skip_defaults=True))
#         try:
#             return self.collection.insert_one(slide.dict(skip_defaults=True))
#         except Exception as e:
#             print("Slide could not be inserted")
#             print(e)
#
#     def update_slide(self, slide_update: UpdateSlide, slide_id: str) -> UpdateResult:
#         """
#         Updates the slide entry with the given values
#
#         :param slide_update: Contains the new values
#         :param slide_id: The slide that should be updated
#         :return: The result of the update operation
#         """
#         slide_query = {"slide_id": slide_id}
#         logging.info(slide_update.dict(skip_defaults=True))
#         values_to_update = {"$set": slide_update.dict(skip_defaults=True)}
#         return self.collection.update_one(slide_query, values_to_update)
#
#     def get_all_slides(self, metadata: bool) -> List[DatabaseSlide]:
#         """
#         Returns all slides stored in the database
#
#         :return: All database entries
#         """
#         if metadata:
#             result = parse_obj_as(List[DatabaseSlide], list(self.collection.find({}, {'_id': False})))
#         else:
#             result = parse_obj_as(List[DatabaseSlideNoMetadata],
#                                   list(self.collection.find({}, {'_id': False, 'metadata': False})))
#         return result
#
#     def get_all_slides_to_ids(self, slide_ids: List[str], metadata: bool) -> List[Slide]:
#         if metadata:
#             result = parse_obj_as(List[DatabaseSlide],
#                                   list(self.collection.find({'slide_id': {'$in': slide_ids}}, {'_id': False})))
#
#         else:
#             result = parse_obj_as(List[DatabaseSlideNoMetadata],
#                                   list(self.collection.find({'slide_id': {'$in': slide_ids}},
#                                                             {'_id': False, 'metadata': False})))
#
#         return result
#
#     def get_slide_with_slide_id(self, slide_id: str) -> Slide:
#         return self.collection.find_one({"slide_id": slide_id})
#
#     def slide_with_name_exists(self, name: str) -> bool:
#         """
#         Checks if slide with the given name already exists
#
#         :param name: slide name to be checked
#         :return: If the slide with the name exists or not
#         """
#         return self.collection.count_documents({'name': name}, limit=1) != 0
#
#     def delete_slide(self, slide_id: str) -> DeleteResult:
#         return self.collection.delete_one({'slide_id': slide_id})
#
#
# slide_db = SlideDatabase()
