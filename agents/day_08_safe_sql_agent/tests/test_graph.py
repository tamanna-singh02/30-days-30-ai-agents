"""Unit tests for Safe SQL Agent LangGraph workflow and nodes."""

import pytest
from agents.day_08_safe_sql_agent.agent.state import SQLAgentState
from agents.day_08_safe_sql_agent.agent.nodes import (
    introspect_schema_node,
    validate_sql_node,
    route_after_validation,
)
from agents.day_08_safe_sql_agent.guardrails.ast_validator import ValidationResult


def test_introspect_schema_node_with_provided_schema():
    state: SQLAgentState = {
        "schema": {
            "users": {
                "columns": [{"name": "id", "type": "integer", "nullable": False}],
                "relationships": [],
            }
        }
    }

    res = introspect_schema_node(state)
    assert res["schema"] == state["schema"]
    assert "TABLE: users" in res["formatted_schema"]


def test_validate_sql_node_valid():
    state: SQLAgentState = {
        "generated_sql": "SELECT id FROM users LIMIT 10",
        "schema": {
            "users": {
                "columns": [{"name": "id", "type": "integer", "nullable": False}],
                "relationships": [],
            }
        },
    }

    res = validate_sql_node(state)
    assert res["validation_result"].allowed is True
    assert res["error"] is None


def test_validate_sql_node_invalid():
    state: SQLAgentState = {
        "generated_sql": "DROP TABLE users",
        "schema": {},
    }

    res = validate_sql_node(state)
    assert res["validation_result"].allowed is False
    assert res["error"] is not None


def test_route_after_validation():
    valid_res = ValidationResult(allowed=True)
    invalid_res = ValidationResult(allowed=False)

    assert route_after_validation({"validation_result": valid_res}) == "execute"
    assert route_after_validation({"validation_result": invalid_res, "retry_count": 1, "max_retries": 3}) == "retry"
    assert route_after_validation({"validation_result": invalid_res, "retry_count": 3, "max_retries": 3}) == "fail"
