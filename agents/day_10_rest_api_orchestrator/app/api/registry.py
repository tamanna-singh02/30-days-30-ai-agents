
from app.models.api import (
    APIDefinition,
    HTTPMethod,
    Parameter,
)


class APIRegistry:

    def __init__(self):
        self._apis: dict[str, APIDefinition] = {}

    def register(self, api: APIDefinition) -> None:
        if api.name in self._apis:
            raise ValueError(
                f"API '{api.name}' is already registered"
            )

        self._apis[api.name] = api

    def get(self, name: str) -> APIDefinition:
        if name not in self._apis:
            raise KeyError(
                f"API '{name}' is not registered"
            )

        return self._apis[name]

    def list_apis(self) -> list[APIDefinition]:
        return list(self._apis.values())

    def search(self, query: str) -> list[APIDefinition]:
        query = query.lower()

        return [
            api
            for api in self._apis.values()
            if (
                query in api.name.lower()
                or query in api.description.lower()
            )
        ]