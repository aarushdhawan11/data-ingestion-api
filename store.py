
import uuid
import time
from collections import deque
from enum import Enum

class Priority(Enum):
    HIGH = 3
    MEDIUM = 2
    LOW = 1

job_queue = deque()
ingestions = {}

def enqueue_job(ids, priority):
    ingestion_id = str(uuid.uuid4())
    timestamp = time.time()
    batches = [ids[i:i+3] for i in range(0, len(ids), 3)]
    batch_data = []
    for batch in batches:
        batch_data.append({
            "batch_id": str(uuid.uuid4()),
            "ids": batch,
            "status": "yet_to_start",
            "priority": Priority[priority],
            "created_time": timestamp
        })
    ingestions[ingestion_id] = {
        "status": "yet_to_start",
        "batches": batch_data
    }
    job_queue.append((Priority[priority], timestamp, ingestion_id))
    return ingestion_id

def get_status(ingestion_id):
    return ingestions.get(ingestion_id)
