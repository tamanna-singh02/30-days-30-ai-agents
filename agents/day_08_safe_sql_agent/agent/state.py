"""State definitions for Safe SQL Agent graph."""

from typing import TypedDict, Optional, Any, Dict


class SQLAgentState(TypedDict, total=False):
    question: str
    schema: Dict[str, Any]
    formatted_schema: str
    generated_sql: str
    validation_result: Any
    execution_result: Any
    error: Optional[str]
    retry_count: int
    max_retries: int
