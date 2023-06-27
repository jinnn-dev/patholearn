from typing import Dict
from bson import ObjectId
from pydantic import parse_obj_as
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import os

from app.schema.dataset import Dataset, DatasetStatus


client: MongoClient = MongoClient(os.environ["DATABASE_URL"])
database: Database = client.ai

dataset_collection: Collection = database.get_collection("dataset")


def update_dataset(dataset_id: str, fields: Dict):
    updated = dataset_collection.update_one(
        {"_id": ObjectId(dataset_id)}, {"$set": fields}
    )
    return updated


def update_dataset_status(dataset_id: str, status: DatasetStatus):
    return update_dataset(dataset_id=dataset_id, fields={"status": status})


def get_dataset(dataset_id: str):
    return parse_obj_as(
        Dataset, dataset_collection.find_one({"_id": ObjectId(dataset_id)})
    )
