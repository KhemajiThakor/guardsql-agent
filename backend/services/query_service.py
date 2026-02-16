import logging
import time

from backend.services.llm import generate_sql
from backend.services.validator import validate_sql
from backend.services.executor import execute_query
from backend.db.connection import get_schema, log_query
from backend.core.exceptions import ValidationError, ExecutionError, LLMError

logger = logging.getLogger(__name__)

async def process_query(question: str) -> dict:
    start_time = time.time()
    schema = get_schema()
    
    try:
        sql = await generate_sql(question, schema)
        validated_sql = validate_sql(sql)
        
        try:
            rows, columns = execute_query(validated_sql)
            exec_time = int((time.time() - start_time) * 1000)
            
            log_query(question, validated_sql, "success", None, exec_time)
            
            return {
                "sql": validated_sql,
                "results": rows,
                "columns": columns,
                "row_count": len(rows),
                "execution_time_ms": exec_time
            }
            
        except ExecutionError as e:
            logger.info("Retrying with error context")
            
            retry_sql = await generate_sql(question, schema, error_context=str(e))
            validated_retry_sql = validate_sql(retry_sql)
            
            rows, columns = execute_query(validated_retry_sql)
            exec_time = int((time.time() - start_time) * 1000)
            
            log_query(question, validated_retry_sql, "success_retry", None, exec_time)
            
            return {
                "sql": validated_retry_sql,
                "results": rows,
                "columns": columns,
                "row_count": len(rows),
                "execution_time_ms": exec_time
            }
    
    except ValidationError as e:
        log_query(question, sql if 'sql' in locals() else "", "validation_error", str(e))
        raise
    except ExecutionError as e:
        log_query(question, validated_retry_sql if 'validated_retry_sql' in locals() else validated_sql, "execution_error", str(e))
        raise
    except LLMError as e:
        log_query(question, "", "llm_error", str(e))
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        log_query(question, "", "error", str(e))
        raise
