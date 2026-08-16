"""Graph nodes for Safe SQL Agent."""

from agents.day_08_safe_sql_agent.agent.state import SQLAgentState
from agents.day_08_safe_sql_agent.database.schema import get_schema, format_schema
from agents.day_08_safe_sql_agent.sql.generator import generate_sql
from agents.day_08_safe_sql_agent.sql.parser import parse_sql
from agents.day_08_safe_sql_agent.guardrails.ast_validator import validate_sql, ValidationResult
from agents.day_08_safe_sql_agent.database.connection import get_connection, get_demo_connection


def introspect_schema_node(state: SQLAgentState) -> SQLAgentState:
    schema = state.get("schema")
    if not schema:
        try:
            schema = get_schema()
        except Exception as e:
            schema = {}

    formatted = state.get("formatted_schema")
    if not formatted:
        formatted = format_schema(schema) if schema else "NO SCHEMA AVAILABLE"

    return {
        "schema": schema,
        "formatted_schema": formatted,
        "retry_count": state.get("retry_count", 0),
        "max_retries": state.get("max_retries", 3),
    }


def generate_sql_node(state: SQLAgentState) -> SQLAgentState:
    question = state.get("question", "")
    formatted_schema = state.get("formatted_schema", "")
    retry_count = state.get("retry_count", 0)

    feedback = None
    prev_result = state.get("validation_result")
    if prev_result and not prev_result.allowed:
        feedback = "; ".join(prev_result.errors)

    sql = generate_sql(user_query=question, schema=formatted_schema, feedback=feedback)

    return {
        "generated_sql": sql,
        "retry_count": retry_count + 1,
    }


def validate_sql_node(state: SQLAgentState) -> SQLAgentState:
    sql = state.get("generated_sql", "")
    schema = state.get("schema", {})

    result = ValidationResult()

    try:
        ast = parse_sql(sql)
        result = validate_sql(ast, schema)
    except Exception as e:
        result.add_error(f"SQL Syntax Error: {str(e)}")

    return {
        "validation_result": result,
        "error": None if result.allowed else "; ".join(result.errors),
    }


def execute_sql_node(state: SQLAgentState) -> SQLAgentState:
    sql = state.get("generated_sql", "")
    result = state.get("validation_result")

    if not result or not result.allowed:
        return {"execution_result": None, "error": "Cannot execute invalid SQL"}

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                cols = [desc[0] for desc in cursor.description]
                formatted_rows = [dict(zip(cols, row)) for row in rows]
                return {"execution_result": formatted_rows, "error": None}
    except Exception:
        try:
            conn = get_demo_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description] if cursor.description else []
            formatted_rows = [dict(zip(cols, row)) for row in rows]
            return {"execution_result": formatted_rows, "error": None}
        except Exception as sqlite_err:
            return {"execution_result": None, "error": f"Execution Error: {str(sqlite_err)}"}



def route_after_validation(state: SQLAgentState) -> str:
    result = state.get("validation_result")
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)

    if result and result.allowed:
        return "execute"
    elif retry_count < max_retries:
        return "retry"
    else:
        return "fail"
