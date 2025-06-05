from fastapi import FastAPI
from models import IngestionRequest
from store import enqueue_job, get_status
import asyncio
from processor import process_batches

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_batches())

@app.post("/ingest")
async def ingest(req: IngestionRequest):
    ingestion_id = enqueue_job(req.ids, req.priority)
    return {"ingestion_id": ingestion_id}

@app.get("/status/{ingestion_id}")
async def status(ingestion_id: str):
    result = get_status(ingestion_id)
    if not result:
        return {"error": "Invalid ingestion_id"}
    return {"ingestion_id": ingestion_id, **result}
