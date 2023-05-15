import os
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import Collection, Database

client: AsyncIOMotorClient = AsyncIOMotorClient(os.environ["DATABASE_URL"])
database: Database = client.ai

test_collection: Collection = database.get_collection("test")
builder_collection: Collection = database.get_collection("builder")
