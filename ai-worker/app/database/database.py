import os
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

client: MongoClient = MongoClient(os.environ["DATABASE_URL"])
database: Database = client.ai

task_collection: Collection = database.get_collection("task")
