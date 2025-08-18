# services/data_loader/mongo_dal.py
import os
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
MONGO_DB   = os.getenv("MONGO_DB", "appdb")
MONGO_USER = os.getenv("MONGO_USER", "appuser")
MONGO_PASS = os.getenv("MONGO_PASS", "apppass")
MONGO_AUTH_SOURCE = os.getenv("MONGO_AUTH_SOURCE", MONGO_DB)

# ניתן גם לספק MONGO_URI ישיר; אם לא, נבנה ממרכיבים
MONGO_URI  = os.getenv(
    "MONGO_URI",
    f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource={MONGO_AUTH_SOURCE}"
)

COLLECTION = os.getenv("MONGO_COLLECTION", "people")

_client: AsyncIOMotorClient | None = None

def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(MONGO_URI)
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
