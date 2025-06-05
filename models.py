
from pydantic import BaseModel
from typing import List, Literal

class IngestionRequest(BaseModel):
    ids: List[int]
    priority: Literal['HIGH', 'MEDIUM', 'LOW']
