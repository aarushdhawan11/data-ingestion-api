
import asyncio
from store import job_queue, ingestions
import time

async def simulate_fetch_data(id):
    await asyncio.sleep(1)
    return {"id": id, "data": "processed"}

async def process_batches():
    while True:
        if not job_queue:
            await asyncio.sleep(1)
            continue

        # sort by priority DESC, then by created_time ASC
        sorted_queue = sorted(job_queue, key=lambda x: (-x[0].value, x[1]))
        job = sorted_queue.pop(0)
        job_queue.remove(job)

        _, _, ingestion_id = job
        ingestion = ingestions[ingestion_id]

        ingestion["status"] = "triggered"
        for batch in ingestion["batches"]:
            if batch["status"] == "completed":
                continue
            batch["status"] = "triggered"
            await asyncio.gather(*[simulate_fetch_data(i) for i in batch["ids"]])
            batch["status"] = "completed"
            await asyncio.sleep(5)  # Rate limiting: 1 batch per 5 sec

        # Update overall status
        if all(b["status"] == "completed" for b in ingestion["batches"]):
            ingestion["status"] = "completed"
        elif any(b["status"] == "triggered" for b in ingestion["batches"]):
            ingestion["status"] = "triggered"
        else:
            ingestion["status"] = "yet_to_start"
