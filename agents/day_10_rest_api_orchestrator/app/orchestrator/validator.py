from app.api.registry import APIRegistry
from app.models.plan import ExecutionPlan


class PlanValidationError(Exception):
    pass


class PlanValidator:

    def __init__(self, registry: APIRegistry):
        self.registry = registry

    def validate(self, plan: ExecutionPlan) -> None:

        self._validate_step_count(plan)

        self._validate_unique_step_ids(plan)

        self._validate_apis(plan)

        self._validate_dependencies(plan)

    def _validate_step_count(
        self,
        plan: ExecutionPlan,
    ) -> None:

        if len(plan.steps) > plan.max_steps:
            raise PlanValidationError(
                f"Plan contains {len(plan.steps)} steps, "
                f"maximum allowed is {plan.max_steps}"
            )

    def _validate_unique_step_ids(
        self,
        plan: ExecutionPlan,
    ) -> None:

        ids = [step.id for step in plan.steps]

        if len(ids) != len(set(ids)):
            raise PlanValidationError(
                "Duplicate step IDs found"
            )

    def _validate_apis(
        self,
        plan: ExecutionPlan,
    ) -> None:

        for step in plan.steps:

            try:
                self.registry.get(step.api)

            except KeyError:
                raise PlanValidationError(
                    f"Unknown API: {step.api}"
                )

    def _validate_dependencies(
        self,
        plan: ExecutionPlan,
    ) -> None:

        step_ids = {
            step.id
            for step in plan.steps
        }

        for step in plan.steps:

            for dependency in step.depends_on:

                if dependency not in step_ids:
                    raise PlanValidationError(
                        f"Step '{step.id}' depends on "
                        f"unknown step '{dependency}'"
                    )