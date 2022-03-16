from typing import Any, Dict, Generic, List, Type, TypeVar

from app.utils.slide_utils import remove_truth_values_from_dict
from bson import ObjectId
from pydantic import BaseModel, parse_obj_as
from pymongo.collection import Collection
from pymongo.results import DeleteResult, UpdateResult

ModelSchemaType = TypeVar("ModelSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelSchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelSchemaType], entity_id_name: str):
        self.model = model
        self.entity_id_name = entity_id_name

    def get_by_objectId(self, collection: Collection, *, object_id: ObjectId) -> ModelSchemaType:
        return parse_obj_as(self.model, collection.find_one({'_id': object_id}))

    def get(self, collection: Collection, *, entity_id_value: Any, filter_qurey: Dict[str, Any] = None) -> ModelSchemaType:
        return parse_obj_as(self.model, collection.find_one({self.entity_id_name: entity_id_value}, remove_truth_values_from_dict(filter_qurey)))

    def get_multi(self, collection: Collection, where_query: Dict[str, Any] = {}, filter_query: Dict[str, Any] = None) -> List[ModelSchemaType]:
        return parse_obj_as(List[self.model], list(collection.find(where_query, remove_truth_values_from_dict(filter_query))))

    def get_multi_by_ids(self, collection: Collection, ids: List[Any], where_query: Dict[str, Any] = {}, filter_query: Dict[str, Any] = None) -> List[
            ModelSchemaType]:
        return parse_obj_as(List[self.model], list(collection.find({self.entity_id_name: {'$in': ids}.update(where_query)},
                                                                   remove_truth_values_from_dict(filter_query))))

    def create(self, collection: Collection, *, obj_in: CreateSchemaType, exclude_unset=True) -> ObjectId:
        return collection.insert_one(obj_in.dict(exclude_unset=exclude_unset)).inserted_id

    def update(self, collection: Collection, *, obj_in: UpdateSchemaType,
               entity_id_value: Any) -> UpdateResult:
        slide_query = {self.entity_id_name: entity_id_value}
        values_to_update = {"$set": obj_in.dict(exclude_unset=True)}
        return collection.update_one(slide_query, values_to_update)

    def delete(self, collection: Collection, *, entity_id_value: Any) -> DeleteResult:
        return collection.delete_one({self.entity_id_name: entity_id_value})
