from app.models.plan import (
    ExecutionPlan,
    ExecutionStep,
)


def test_execution_plan():

    plan = ExecutionPlan(
        goal="Find the user's pending orders and cancel the latest one",

        steps=[
            ExecutionStep(
                id="get_orders",
                api="get_user_orders",
                parameters={
                    "user_id": "42"
                },
            ),

            ExecutionStep(
                id="cancel_order",
                api="cancel_order",
                parameters={
                    "order_id": "{{get_orders.latest_pending.id}}"
                },
                depends_on=[
                    "get_orders"
                ],
            ),
        ],
    )

    print(plan.model_dump_json(indent=2))