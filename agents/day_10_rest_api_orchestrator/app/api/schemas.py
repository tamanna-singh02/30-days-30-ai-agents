
from app.api.registry import APIRegistry
from app.models.api import (
    APIDefinition,
    HTTPMethod,
    Parameter,
)


def create_api_registry() -> APIRegistry:

    registry = APIRegistry()

    registry.register(
        APIDefinition(
            name="get_user",
            description="Get details of a user by their user ID",
            method=HTTPMethod.GET,
            path="/users/{user_id}",
            parameters=[
                Parameter(
                    name="user_id",
                    description="Unique identifier of the user",
                )
            ],
            response_schema={
                "id": "integer",
                "name": "string",
                "email": "string",
            },
        )
    )

    registry.register(
        APIDefinition(
            name="get_user_orders",
            description="Get all orders belonging to a user",
            method=HTTPMethod.GET,
            path="/users/{user_id}/orders",
            parameters=[
                Parameter(
                    name="user_id",
                    description="Unique identifier of the user",
                )
            ],
            response_schema={
                "orders": "array",
            },
        )
    )

    registry.register(
        APIDefinition(
            name="cancel_order",
            description="Cancel an existing order",
            method=HTTPMethod.POST,
            path="/orders/{order_id}/cancel",
            parameters=[
                Parameter(
                    name="order_id",
                    description="Unique identifier of the order",
                )
            ],
            response_schema={
                "success": "boolean",
                "message": "string",
            },
        )
    )

    return registry