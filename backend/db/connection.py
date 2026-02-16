import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from backend.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_query_logs():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS query_logs (
                id SERIAL PRIMARY KEY,
                question TEXT NOT NULL,
                generated_sql TEXT,
                status VARCHAR(50) NOT NULL,
                error_message TEXT,
                execution_time_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.commit()
    logger.info("Query logs table initialized")

def log_query(question: str, sql: str, status: str, error: str = None, exec_time: int = None):
    try:
        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO query_logs 
                    (question, generated_sql, status, error_message, execution_time_ms)
                    VALUES (:q, :sql, :status, :error, :time)
                """),
                {"q": question, "sql": sql, "status": status, "error": error, "time": exec_time}
            )
            conn.commit()
    except Exception as e:
        logger.error(f"Failed to log query: {e}")

def get_schema() -> str:
    inspector = inspect(engine)
    schema_parts = []
    
    for table in inspector.get_table_names():
        if table in ['query_logs', 'pg_stat_statements']:
            continue
        
        cols = inspector.get_columns(table)
        col_defs = [f"  {c['name']} {c['type']}" for c in cols]
        schema_parts.append(f"Table: {table}\n" + "\n".join(col_defs))
    
    return "\n\n".join(schema_parts)

def check_db_health() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
