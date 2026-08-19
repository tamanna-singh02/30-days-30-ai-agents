from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class StepResult(BaseModel):
    step_id: str

    status: StepStatus

    status_code: int | None = None

    data: Any = None

    error: str | None = None


class ExecutionState(BaseModel):

    results: dict[str, StepResult] = Field(
        default_factory=dict
    )

    def add_result(
        self,
        result: StepResult,
    ) -> None:

        self.results[result.step_id] = result

    def get_result(
        self,
        step_id: str,
    ) -> StepResult:

        return self.results[step_id]