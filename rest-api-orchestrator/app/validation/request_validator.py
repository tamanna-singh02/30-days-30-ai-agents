from typing import Any
from app.models.api import APIDefinition, Parameter


class RequestValidationError(Exception):
    pass


class RequestValidator:
    def validate(self, api: APIDefinition, parameters: dict[str, Any]) -> None:
        """
        Validates parameter presence and types against the API definition.
        """
        # Check required parameters
        for param in api.parameters:
            if param.required and param.name not in parameters:
                raise RequestValidationError(
                    f"API '{api.name}' requires parameter '{param.name}' ({param.description})"
                )

        # Validate types if parameter present
        for name, value in parameters.items():
            param_def = next((p for p in api.parameters if p.name == name), None)
            if param_def and param_def.type:
                self._validate_type(api.name, name, value, param_def.type)

    def _validate_type(self, api_name: str, param_name: str, value: Any, expected_type: str) -> None:
        expected_type_lower = expected_type.lower()
        if expected_type_lower in ("int", "integer") and not isinstance(value, int):
            try:
                int(value)
            except (ValueError, TypeError):
                raise RequestValidationError(
                    f"API '{api_name}' parameter '{param_name}' expected integer, got '{type(value).__name__}'"
                )
        elif expected_type_lower in ("bool", "boolean") and not isinstance(value, bool):
            if str(value).lower() not in ("true", "false", "1", "0"):
                raise RequestValidationError(
                    f"API '{api_name}' parameter '{param_name}' expected boolean, got '{type(value).__name__}'"
                )
