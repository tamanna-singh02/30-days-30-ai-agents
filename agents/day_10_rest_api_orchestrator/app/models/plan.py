
from typing import Any

from pydantic import BaseModel, Field


class ExecutionStep(BaseModel):
    id: str = Field(
        description="Unique identifier for this execution step"
    )

    api: str = Field(
        description="Name of the API from the API registry"
    )

    parameters: dict[str, Any] = Field(
        default_factory=dict
    )

    depends_on: list[str] = Field(
        default_factory=list
    )

    condition: str | None = None


class ExecutionPlan(BaseModel):
    goal: str

    steps: list[ExecutionStep]

    max_steps: int = 10