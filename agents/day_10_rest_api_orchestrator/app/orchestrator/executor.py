from typing import Any
from app.api.client import APIClient
from app.api.registry import APIRegistry
from app.models.plan import ExecutionStep
from app.orchestrator.resolver import ReferenceResolver
from app.orchestrator.state import ExecutionState, StepResult, StepStatus
from app.resilience.retry import RetryPolicy
from app.resilience.timeout import TimeoutHandler
from app.validation.request_validator import RequestValidator
from app.validation.response_validator import ResponseValidator


class StepExecutor:
    def __init__(
        self,
        registry: APIRegistry,
        client: APIClient,
        request_validator: RequestValidator | None = None,
        response_validator: ResponseValidator | None = None,
    ):
        self.registry = registry
        self.client = client
        self.request_validator = request_validator or RequestValidator()
        self.response_validator = response_validator or ResponseValidator()

    async def execute_step(
        self,
        step: ExecutionStep,
        state: ExecutionState,
    ) -> StepResult:
        api = self.registry.get(step.api)

        # 1. Resolve references in parameter values
        resolver = ReferenceResolver(state)
        parameters: dict[str, Any] = {
            key: resolver.resolve(val)
            for key, val in step.parameters.items()
        }

        # 2. Validate request parameters
        try:
            self.request_validator.validate(api, parameters)
        except Exception as val_err:
            return StepResult(
                step_id=step.id,
                status=StepStatus.FAILED,
                error=f"Request validation failed: {val_err}",
            )

        # 3. Setup resilience handlers
        timeout_handler = TimeoutHandler(timeout_seconds=api.timeout)
        retry_policy = RetryPolicy(max_retries=api.retry_count)

        async def _call_api() -> tuple[int, Any]:
            return await timeout_handler.execute(
                self.client.execute(api, parameters),
                step_name=step.id,
            )

        try:
            # 4. Execute with retry & timeout
            status_code, data = await retry_policy.execute(_call_api, step_name=step.id)

            # 5. Validate response
            self.response_validator.validate(api, status_code, data)

            return StepResult(
                step_id=step.id,
                status=StepStatus.SUCCESS,
                status_code=status_code,
                data=data,
            )

        except Exception as exc:
            return StepResult(
                step_id=step.id,
                status=StepStatus.FAILED,
                error=str(exc),
            )
