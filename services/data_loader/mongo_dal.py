# services/data_loader/mongo_dal.py
import os
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient

from .config import mongo_uri

MONGO_DB = os.getenv("MONGO_DB", "appdb")

COLLECTION = os.getenv("MONGO_COLLECTION", "people")

_client: AsyncIOMotorClient | None = None

def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(mongo_uri())
    return _client

def get_collection():
    cli = get_client()
    return cli[MONGO_DB][COLLECTION]

async def list_people() -> List[Dict[str, Any]]:
    col = get_collection()
    docs = []
    async for d in col.find({}, {"_id": 0}):  # מסיר _id להחזרה נקייה
        docs.append(d)
    return docs

async def insert_person(first_name: str, last_name: str) -> Dict[str, Any]:
    col = get_collection()
    doc = {"first_name": first_name, "last_name": last_name}
    await col.insert_one(doc)
    return doc

async def ensure_indexes():
    col = get_collection()
    await col.create_index([("last_name", 1)])

async def close_client():
    global _client
    if _client is not None:
        _client.close()
        _client = None
