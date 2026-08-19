from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class Parameter(BaseModel):
    name: str
    type: str = "string"
    description: str
    required: bool = False

class APIDefinition(BaseModel):
    name: str
    description: str

    method: HTTPMethod
    path: str

    parameters: list[Parameter] = Field(default_factory=list)

    request_schema: dict[str, Any] | None = None
    response_schema: dict[str, Any] | None = None

    timeout: float = 10.0
    retry_count: int = 2

    requires_auth: bool = True
