from app.database.database import task_collection
from bson import ObjectId


def update_version_status(task_id: str, version_id: str, status: str):
    task_collection.update_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
        },
        {"$set": {"versions.$[version].status": status}},
        array_filters=[{"version.id": ObjectId(version_id)}],
    )


def update_version_clearml_id(task_id: str, version_id: str, clearml_id: str):
    task_collection.update_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
        },
        {"$set": {"versions.$[version].clearml_id": clearml_id}},
        array_filters=[{"version.id": ObjectId(version_id)}],
    )


def update_version_dataset_id(task_id: str, version_id: str, dataset_id: str):
    task_collection.update_one(
        {
            "_id": ObjectId(task_id),
            "versions": {"$elemMatch": {"id": ObjectId(version_id)}},
        },
        {"$set": {"versions.$[version].dataset_id": dataset_id}},
        array_filters=[{"version.id": ObjectId(version_id)}],
    )
