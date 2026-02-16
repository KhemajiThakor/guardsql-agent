from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from backend.api.routes import router
from backend.core.logging import setup_logging
from backend.core.config import get_settings
from backend.db.connection import init_query_logs
from backend.core.exceptions import GuardSQLException

setup_logging()
logger = logging.getLogger(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting GuardSQL API")
    try:
        init_query_logs()
        logger.info("Application started")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
    yield
    logger.info("Shutting down")

app = FastAPI(
    title="GuardSQL",
    description="Secure SQL query generator from natural language",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.exception_handler(GuardSQLException)
async def guardsql_exception_handler(request: Request, exc: GuardSQLException):
    return JSONResponse(
        status_code=400,
        content={"error": exc.__class__.__name__, "detail": str(exc)}
    )

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
        log_level=settings.log_level.lower()
    )
