import asyncio
from typing import Awaitable, TypeVar

T = TypeVar("T")


class TimeoutError(Exception):
    pass


class TimeoutHandler:
    def __init__(self, timeout_seconds: float = 10.0):
        self.timeout_seconds = timeout_seconds

    async def execute(self, coro: Awaitable[T], step_name: str = "step") -> T:
        try:
            return await asyncio.wait_for(coro, timeout=self.timeout_seconds)
        except asyncio.TimeoutError:
            raise TimeoutError(f"[{step_name}] Execution timed out after {self.timeout_seconds}s")
