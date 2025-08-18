# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from services.data_loader.mongo_dal import list_people, insert_person, ensure_indexes, close_client

app = FastAPI(title="Data Loader API (MongoDB)")

class PersonIn(BaseModel):
    first_name: str
    last_name: str

@app.on_event("startup")
async def on_startup():
    await ensure_indexes()

@app.on_event("shutdown")
async def on_shutdown():
    await close_client()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/data")
async def get_data():
    return await list_people()

@app.post("/data")
async def add_person(p: PersonIn):
    return await insert_person(p.first_name, p.last_name)
