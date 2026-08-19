import asyncio
import logging
from typing import Callable, TypeVar, Awaitable

logger = logging.getLogger("resilience.retry")
T = TypeVar("T")


class RetryPolicy:
    def __init__(self, max_retries: int = 3, initial_delay: float = 0.5, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor

    async def execute(self, func: Callable[[], Awaitable[T]], step_name: str = "step") -> T:
        delay = self.initial_delay
        last_exception = None

        for attempt in range(1, self.max_retries + 1):
            try:
                return await func()
            except Exception as exc:
                last_exception = exc
                if attempt == self.max_retries:
                    logger.warning(f"[{step_name}] Retry limit reached ({self.max_retries} attempts). Error: {exc}")
                    raise exc
                logger.info(f"[{step_name}] Attempt {attempt} failed ({exc}). Retrying in {delay:.2f}s...")
                await asyncio.sleep(delay)
                delay *= self.backoff_factor

        if last_exception:
            raise last_exception
        raise RuntimeError(f"[{step_name}] Retries exhausted")
