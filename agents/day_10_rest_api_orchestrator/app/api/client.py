
from typing import Any

import httpx

from app.models.api import APIDefinition


class APIClient:

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def execute(
        self,
        api: APIDefinition,
        parameters: dict[str, Any],
    ) -> tuple[int, Any]:

        path = api.path

        for name, value in parameters.items():
            path = path.replace(
                f"{{{name}}}",
                str(value),
            )

        url = f"{self.base_url}{path}"

        async with httpx.AsyncClient(
            timeout=api.timeout
        ) as client:

            response = await client.request(
                method=api.method.value,
                url=url,
            )

            try:
                data = response.json()
            except ValueError:
                data = response.text

            return response.status_code, data