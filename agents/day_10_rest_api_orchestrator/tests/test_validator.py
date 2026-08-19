import pytest

from app.api.schemas import create_api_registry
from app.models.plan import (
    ExecutionPlan,
    ExecutionStep,
)
from app.orchestrator.validator import (
    PlanValidator,
    PlanValidationError,
)


def test_valid_plan():

    registry = create_api_registry()

    validator = PlanValidator(registry)

    plan = ExecutionPlan(
        goal="Get user orders",
        steps=[
            ExecutionStep(
                id="orders",
                api="get_user_orders",
                parameters={
                    "user_id": "42"
                },
            )
        ],
    )

    validator.validate(plan)


def test_unknown_api():

    registry = create_api_registry()

    validator = PlanValidator(registry)

    plan = ExecutionPlan(
        goal="Do something",
        steps=[
            ExecutionStep(
                id="unknown",
                api="delete_everything",
            )
        ],
    )

    with pytest.raises(PlanValidationError):

        validator.validate(plan)

def _validate_dependencies(
    self,
    plan: ExecutionPlan,
) -> None:

    step_ids = {
        step.id
        for step in plan.steps
    }

    graph = {
        step.id: step.depends_on
        for step in plan.steps
    }

    for step in plan.steps:

        for dependency in step.depends_on:

            if dependency not in step_ids:
                raise PlanValidationError(
                    f"Step '{step.id}' depends on "
                    f"unknown step '{dependency}'"
                )

    self._detect_cycles(graph)


def _detect_cycles(
    self,
    graph: dict[str, list[str]],
) -> None:

    visiting = set()
    visited = set()

    def visit(node: str):

        if node in visiting:
            raise PlanValidationError(
                "Circular dependency detected"
            )

        if node in visited:
            return

        visiting.add(node)

        for dependency in graph[node]:
            visit(dependency)

        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)