import asyncio

from app.api.client import APIClient
from app.api.registry import APIRegistry
from app.models.plan import ExecutionPlan, ExecutionStep

from app.orchestrator.dependency import (
    DependencyResolver,
)

from app.orchestrator.resolver import (
    ReferenceResolver,
)

from app.orchestrator.state import (
    ExecutionState,
    StepResult,
    StepStatus,
)


class Orchestrator:

    def __init__(
        self,
        registry: APIRegistry,
        client: APIClient,
    ):

        self.registry = registry
        self.client = client

    async def execute(
        self,
        plan: ExecutionPlan,
    ) -> ExecutionState:

        state = ExecutionState()

        completed: set[str] = set()
        failed: set[str] = set()

        resolver = DependencyResolver()

        while len(completed) + len(failed) < len(
            plan.steps
        ):

            ready_steps = resolver.get_ready_steps(
                plan,
                completed,
                failed,
            )

            if not ready_steps:

                remaining = [
                    step.id
                    for step in plan.steps
                    if step.id not in completed
                    and step.id not in failed
                ]

                if remaining:

                    raise RuntimeError(
                        "Unable to make progress. "
                        f"Remaining steps: {remaining}"
                    )

                break

            results = await asyncio.gather(
                *[
                    self._execute_step(
                        step,
                        state,
                    )
                    for step in ready_steps
                ],
                return_exceptions=False,
            )

            for result in results:

                state.add_result(result)

                if (
                    result.status
                    == StepStatus.SUCCESS
                ):

                    completed.add(
                        result.step_id
                    )

                else:

                    failed.add(
                        result.step_id
                    )

        return state

    async def _execute_step(
        self,
        step: ExecutionStep,
        state: ExecutionState,
    ) -> StepResult:

        api = self.registry.get(
            step.api
        )

        resolver = ReferenceResolver(
            state
        )

        parameters = {
            key: resolver.resolve(value)
            for key, value
            in step.parameters.items()
        }

        try:

            status_code, data = (
                await self.client.execute(
                    api,
                    parameters,
                )
            )

            success = (
                200 <= status_code < 300
            )

            return StepResult(
                step_id=step.id,
                status=(
                    StepStatus.SUCCESS
                    if success
                    else StepStatus.FAILED
                ),
                status_code=status_code,
                data=data,
            )

        except Exception as exc:

            return StepResult(
                step_id=step.id,
                status=StepStatus.FAILED,
                error=str(exc),
            )