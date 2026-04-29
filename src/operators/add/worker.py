"""Addition operator worker."""

import asyncio
import logging

from temporal_worker_sdk import TemporalSDK

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


async def main():
    sdk = TemporalSDK()
    sdk.register_activities(add)
    await sdk.start()


if __name__ == "__main__":
    asyncio.run(main())
