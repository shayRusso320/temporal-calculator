"""Division operator worker."""

import asyncio
import logging

from temporalio import activity
from temporal_worker_sdk import TemporalSDK

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class DivisionByZeroError(Exception):
    """Raised when attempting to divide by zero."""
    pass


@activity.defn
async def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise DivisionByZeroError("Cannot divide by zero")
    return a / b


async def main():
    sdk = TemporalSDK()
    sdk.register_activities(divide)
    await sdk.start()


if __name__ == "__main__":
    asyncio.run(main())