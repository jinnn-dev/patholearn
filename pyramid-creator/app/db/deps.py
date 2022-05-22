import os
from collections import Collection, Generator
from sqlite3 import connect

from pymongo import MongoClient

DB = os.getenv("MONGO_DB") if "MONGO_DB" in os.environ else "slidedb"


def get_slide_collection() -> Generator:
    global client

    try:
        client = MongoClient(
            os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=5000, connect=False
        )
        yield client[DB]["slides"]
    finally:
        client.close()


def get_task_image_collection() -> Generator:
    global client

    try:
        client = MongoClient(
            os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=5000, connect=False
        )
        yield client[DB]["task-images"]
    finally:
        client.close()


def get_info_image_collection() -> Generator:
    global client

    try:
        client = MongoClient(
            os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=5000, connect=False
        )
        yield client[DB]["info-images"]
    finally:
        client.close()


def get_slide_collection_no_generator() -> Collection:
    client = MongoClient(
        os.getenv("DATABASE_URL"), serverSelectionTimeoutMS=5000, connect=False
    )
    return client[DB]["slides"]
