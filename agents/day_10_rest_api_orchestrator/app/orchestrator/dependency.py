from app.models.plan import ExecutionPlan, ExecutionStep


class DependencyResolver:

    def get_ready_steps(
        self,
        plan: ExecutionPlan,
        completed: set[str],
        failed: set[str],
    ) -> list[ExecutionStep]:

        ready = []

        for step in plan.steps:

            if step.id in completed:
                continue

            # Don't execute a step if one of its
            # dependencies failed.
            if any(
                dependency in failed
                for dependency in step.depends_on
            ):
                continue

            if all(
                dependency in completed
                for dependency in step.depends_on
            ):
                ready.append(step)

        return ready