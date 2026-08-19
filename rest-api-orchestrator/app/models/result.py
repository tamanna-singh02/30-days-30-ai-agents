from typing import Any
from pydantic import BaseModel, Field
from app.orchestrator.state import ExecutionState, StepResult, StepStatus


class OrchestrationResult(BaseModel):
    goal: str
    success: bool
    total_steps: int
    successful_steps: int
    failed_steps: int
    skipped_steps: int
    results: dict[str, StepResult] = Field(default_factory=dict)
    error: str | None = None

    @classmethod
    def from_state(cls, goal: str, state: ExecutionState, error: str | None = None) -> "OrchestrationResult":
        total = len(state.results)
        successful = sum(1 for r in state.results.values() if r.status == StepStatus.SUCCESS)
        failed = sum(1 for r in state.results.values() if r.status == StepStatus.FAILED)
        skipped = sum(1 for r in state.results.values() if r.status == StepStatus.SKIPPED)

        return cls(
            goal=goal,
            success=failed == 0 and error is None,
            total_steps=total,
            successful_steps=successful,
            failed_steps=failed,
            skipped_steps=skipped,
            results=state.results,
            error=error,
        )
