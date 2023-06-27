from typing import Dict
from bson import ObjectId
from pydantic import parse_obj_as
from app.schema.dataset import Dataset, DatasetStatus
from app.database.database import dataset_collection


async def update_dataset(dataset_id: str, fiedls: Dict):
    updated_dataset = await dataset_collection.update_one(
        {"_id": ObjectId(dataset_id)}, {"$set": fiedls}
    )
    return updated_dataset


async def update_dataset_status(dataset_id: str, status: DatasetStatus):
    return await update_dataset(ObjectId(dataset_id), {"status": status})


async def get_dataset(dataset_id: str) -> Dataset:
    dataset = await dataset_collection.find_one({"_id": ObjectId(dataset_id)})
    return parse_obj_as(Dataset, dataset)
