import os
from collections import Generator, Collection

from pymongo import MongoClient

DB = "slidedb"

def get_slide_collection() -> Generator:
    global client

    try:
        client = MongoClient(os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=5000, connect=False)
        yield client[DB]["slides"]
    finally:
        client.close()


def get_task_image_collection() -> Generator:
    global client

    try:
        client = MongoClient(os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=5000, connect=False)
        yield client[DB]["task-images"]
    finally:
        client.close()


def get_slide_collection_no_generator() -> Collection:
    client = MongoClient(os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=5000, connect=False)
    return client[DB]["slides"]
