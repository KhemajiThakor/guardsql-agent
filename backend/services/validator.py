import sqlglot
import logging
import re
from sqlglot import parse_one, exp

from backend.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE",
    "TRUNCATE", "GRANT", "REVOKE", "EXEC", "EXECUTE", "CALL"
]

SYSTEM_TABLES = ["pg_", "information_schema"]

def validate_sql(sql: str) -> str:
    sql = sql.strip().rstrip(";")
    
    if ";" in sql:
        raise ValidationError("Multiple statements not allowed")
    
    sql_upper = sql.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf'\b{keyword}\b', sql_upper):
            raise ValidationError(f"Forbidden keyword: {keyword}")
    
    try:
        parsed = parse_one(sql, read="postgres")
    except Exception as e:
        raise ValidationError(f"Invalid SQL syntax: {str(e)}")
    
    if not isinstance(parsed, exp.Select):
        raise ValidationError("Only SELECT queries allowed")
    
    for table in SYSTEM_TABLES:
        if table in sql.lower():
            raise ValidationError(f"Access to system tables not allowed")
    
    if "LIMIT" not in sql_upper:
        sql = f"{sql} LIMIT 100"
        logger.info("Auto-appended LIMIT 100")
    
    return sql
