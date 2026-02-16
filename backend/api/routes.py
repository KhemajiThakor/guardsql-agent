from fastapi import APIRouter, Depends, HTTPException
import logging

from backend.api.schemas import QueryRequest, QueryResponse, HealthResponse
from backend.api.auth import verify_credentials
from backend.services.query_service import process_query
from backend.db.connection import check_db_health
from backend.core.exceptions import ValidationError, ExecutionError, LLMError

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    db_healthy = check_db_health()
    return HealthResponse(
        status="healthy" if db_healthy else "degraded",
        database=db_healthy
    )

@router.get("/ready", response_model=HealthResponse)
async def readiness_check():
    db_healthy = check_db_health()
    if not db_healthy:
        raise HTTPException(status_code=503, detail="Database not ready")
    return HealthResponse(status="ready", database=True)

@router.post("/query", response_model=QueryResponse)
async def execute_query(
    request: QueryRequest,
    _: bool = Depends(verify_credentials)
):
    try:
        result = await process_query(request.question)
        return QueryResponse(**result)
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except ExecutionError as e:
        logger.error(f"Execution error: {e}")
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
    except LLMError as e:
        logger.error(f"LLM error: {e}")
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
