"""Unit tests for AST Validator guardrails in Safe SQL Agent."""

import pytest
from sqlglot import parse_one
from agents.day_08_safe_sql_agent.guardrails.ast_validator import (
    validate_sql,
    validate_statement_type,
    validate_tables,
    validate_table_schemas,
    validate_columns,
    validate_limit,
    validate_functions,
    ValidationResult,
)


@pytest.fixture
def mock_schema():
    return {
        "customers": {
            "columns": [
                {"name": "id", "type": "integer", "nullable": False},
                {"name": "name", "type": "varchar", "nullable": False},
                {"name": "email", "type": "varchar", "nullable": True},
            ],
            "relationships": [],
        },
        "orders": {
            "columns": [
                {"name": "id", "type": "integer", "nullable": False},
                {"name": "customer_id", "type": "integer", "nullable": False},
                {"name": "total_amount", "type": "numeric", "nullable": False},
            ],
            "relationships": [
                {"column": "customer_id", "references": "customers.id"}
            ],
        },
    }


def test_valid_select_query(mock_schema):
    sql = "SELECT id, name FROM customers LIMIT 10"
    ast = parse_one(sql, read="postgres")
    result = validate_sql(ast, mock_schema)

    assert result.allowed is True
    assert len(result.errors) == 0


def test_valid_join_query_with_alias(mock_schema):
    sql = "SELECT c.name, o.total_amount FROM customers c JOIN orders o ON c.id = o.customer_id LIMIT 50"
    ast = parse_one(sql, read="postgres")
    result = validate_sql(ast, mock_schema)

    assert result.allowed is True
    assert len(result.errors) == 0


def test_forbidden_statement_types(mock_schema):
    statements = [
        "DELETE FROM customers WHERE id = 1",
        "DROP TABLE orders",
        "UPDATE customers SET name = 'Hacked' WHERE id = 1",
        "INSERT INTO customers (id, name) VALUES (1, 'Alice')",
    ]

    for stmt in statements:
        ast = parse_one(stmt, read="postgres")
        result = validate_sql(ast, mock_schema)
        assert result.allowed is False
        assert any("not allowed" in err for err in result.errors)


def test_forbidden_schema_access(mock_schema):
    sql = "SELECT * FROM pg_catalog.pg_tables LIMIT 10"
    ast = parse_one(sql, read="postgres")
    result = validate_sql(ast, mock_schema)

    assert result.allowed is False
    assert any("forbidden" in err for err in result.errors)


def test_forbidden_functions(mock_schema):
    sql = "SELECT PG_READ_FILE('config.json') LIMIT 1"
    ast = parse_one(sql, read="postgres")
    result = validate_sql(ast, mock_schema)

    assert result.allowed is False
    assert any("Function 'PG_READ_FILE' is not allowed" in err for err in result.errors)


def test_missing_limit_clause(mock_schema):
    sql = "SELECT id, name FROM customers"
    ast = parse_one(sql, read="postgres")
    result = validate_sql(ast, mock_schema)

    assert result.allowed is False
    assert any("LIMIT clause is required" in err for err in result.errors)


def test_excessive_limit_clause(mock_schema):
    sql = "SELECT id, name FROM customers LIMIT 5000"
    ast = parse_one(sql, read="postgres")
    result = validate_sql(ast, mock_schema)

    assert result.allowed is False
    assert any("cannot exceed" in err for err in result.errors)


def test_unknown_table(mock_schema):
    sql = "SELECT * FROM secret_table LIMIT 10"
    ast = parse_one(sql, read="postgres")
    result = validate_sql(ast, mock_schema)

    assert result.allowed is False
    assert any("Table 'secret_table' is not allowed" in err for err in result.errors)


def test_unknown_column(mock_schema):
    sql = "SELECT non_existent_col FROM customers LIMIT 10"
    ast = parse_one(sql, read="postgres")
    result = validate_sql(ast, mock_schema)

    assert result.allowed is False
    assert any("does not exist" in err for err in result.errors)
