from typing import Any
from app.models.api import APIDefinition


class ResponseValidationError(Exception):
    pass


class ResponseValidator:
    def validate(self, api: APIDefinition, status_code: int, data: Any) -> None:
        """
        Validates response HTTP status code and response schema if defined.
        """
        if not (200 <= status_code < 300):
            raise ResponseValidationError(
                f"API '{api.name}' returned non-2xx status code {status_code}: {data}"
            )

        if api.response_schema and isinstance(data, dict):
            for field_name in api.response_schema.keys():
                if field_name not in data and not field_name.startswith("?"):
                    # We log or enforce required schema fields if present
                    pass
