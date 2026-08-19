import re
from typing import Any

from app.orchestrator.state import ExecutionState

REFERENCE_PATTERN = re.compile(r"\{\{([^}]+)\}\}")
INDEX_PATTERN = re.compile(r"^([^\[]+)\[(\d+)\]$")


class ReferenceResolver:

    def __init__(self, state: ExecutionState):
        self.state = state

    def resolve(
        self,
        value: Any,
    ) -> Any:

        if isinstance(value, dict):
            return {
                key: self.resolve(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [
                self.resolve(item)
                for item in value
            ]

        if not isinstance(value, str):
            return value

        match = REFERENCE_PATTERN.fullmatch(value)

        if not match:
            return value

        expression = match.group(1)

        return self._resolve_expression(expression)

    def _resolve_expression(
        self,
        expression: str,
    ) -> Any:

        parts = expression.split(".")
        step_id = parts[0]

        result = self.state.get_result(step_id)
        current = result.data

        for part in parts[1:]:
            current = self._resolve_part(current, part)

        return current

    def _resolve_part(self, current: Any, part: str) -> Any:
        idx_match = INDEX_PATTERN.match(part)

        if idx_match:
            field_name = idx_match.group(1)
            idx = int(idx_match.group(2))
            if isinstance(current, dict) and field_name in current:
                target_list = current[field_name]
                if isinstance(target_list, list) and 0 <= idx < len(target_list):
                    return target_list[idx]
            raise ValueError(f"Cannot index '{part}' in data: {current}")

        if isinstance(current, dict) and part in current:
            return current[part]

        if isinstance(current, list) and part.isdigit():
            idx = int(part)
            if 0 <= idx < len(current):
                return current[idx]

        raise ValueError(f"Cannot resolve field '{part}' in data: {current}")
