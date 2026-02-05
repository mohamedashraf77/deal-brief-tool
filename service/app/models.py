from pydantic import BaseModel, Field
from typing import List


class Entities(BaseModel):
    company: str
    founders: List[str]
    sector: str
    geography: str
    stage: str
    round_size: str
    notable_metrics: List[str]


class DealBrief(BaseModel):
    investment_brief: List[str] = Field(..., min_items=5, max_items=10)
    entities: Entities
    tags: List[str]
