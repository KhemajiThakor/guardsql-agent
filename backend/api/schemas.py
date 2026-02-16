from typing import List, Optional
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)

class QueryResponse(BaseModel):
    sql: str
    results: List[dict]
    columns: List[str]
    row_count: int
    execution_time_ms: int

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    database: bool
    ollama: bool = None
