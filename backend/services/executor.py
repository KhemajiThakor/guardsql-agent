import logging
from sqlalchemy import text

from backend.db.connection import engine
from backend.core.exceptions import ExecutionError

logger = logging.getLogger(__name__)

def execute_query(sql: str) -> tuple[list[dict], list[str]]:
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = list(result.keys())
            rows = [dict(row._mapping) for row in result.fetchall()]
            
            logger.info(f"Query executed: {len(rows)} rows returned")
            return rows, columns
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Query execution failed: {error_msg}")
        raise ExecutionError(error_msg)
