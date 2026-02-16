import pytest

from backend.services.validator import validate_sql
from backend.core.exceptions import ValidationError

def test_valid_select():
    sql = "SELECT * FROM customers WHERE state = 'CA'"
    result = validate_sql(sql)
    assert "LIMIT 100" in result
    assert result.startswith("SELECT")

def test_forbidden_keywords():
    forbidden_queries = [
        "DELETE FROM customers",
        "UPDATE customers SET name = 'test'",
        "DROP TABLE customers",
        "INSERT INTO customers VALUES (1, 'test')",
        "CREATE TABLE test (id INT)",
        "TRUNCATE TABLE customers",
    ]
    
    for query in forbidden_queries:
        with pytest.raises(ValidationError):
            validate_sql(query)

def test_multiple_statements():
    sql = "SELECT * FROM customers; DROP TABLE customers;"
    with pytest.raises(ValidationError, match="Multiple statements"):
        validate_sql(sql)

def test_system_tables():
    sql = "SELECT * FROM pg_tables"
    with pytest.raises(ValidationError, match="system tables"):
        validate_sql(sql)

def test_auto_limit():
    sql = "SELECT * FROM customers"
    result = validate_sql(sql)
    assert "LIMIT 100" in result

def test_existing_limit():
    sql = "SELECT * FROM customers LIMIT 50"
    result = validate_sql(sql)
    assert result.count("LIMIT") == 1

def test_invalid_syntax():
    sql = "SELECT * FORM customers"
    with pytest.raises(ValidationError, match="Invalid SQL"):
        validate_sql(sql)

def test_non_select():
    sql = "SHOW TABLES"
    with pytest.raises(ValidationError, match="Only SELECT"):
        validate_sql(sql)
