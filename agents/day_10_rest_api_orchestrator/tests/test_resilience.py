import asyncio
import pytest
from app.resilience.retry import RetryPolicy
from app.resilience.timeout import TimeoutHandler, TimeoutError


@pytest.mark.asyncio
async def test_retry_policy_success():
    policy = RetryPolicy(max_retries=3, initial_delay=0.01)
    attempts = 0

    async def _flaky_op():
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise ValueError("Temporary failure")
        return "success"

    result = await policy.execute(_flaky_op, step_name="test_flaky")
    assert result == "success"
    assert attempts == 2


@pytest.mark.asyncio
async def test_retry_policy_exhausted():
    policy = RetryPolicy(max_retries=2, initial_delay=0.01)

    async def _always_fails():
        raise ValueError("Permanent failure")

    with pytest.raises(ValueError, match="Permanent failure"):
        await policy.execute(_always_fails, step_name="test_fail")


@pytest.mark.asyncio
async def test_timeout_handler_success():
    handler = TimeoutHandler(timeout_seconds=1.0)

    async def _fast_op():
        await asyncio.sleep(0.01)
        return "done"

    res = await handler.execute(_fast_op(), step_name="fast")
    assert res == "done"


@pytest.mark.asyncio
async def test_timeout_handler_exceeded():
    handler = TimeoutHandler(timeout_seconds=0.05)

    async def _slow_op():
        await asyncio.sleep(0.2)

    with pytest.raises(TimeoutError):
        await handler.execute(_slow_op(), step_name="slow")
