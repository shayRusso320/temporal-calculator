"""Subtraction operator worker."""

import asyncio
import logging

from temporal_worker_sdk import TemporalSDK

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b


async def main():
    sdk = TemporalSDK()
    sdk.register_activities(subtract)
    await sdk.start()


if __name__ == "__main__":
    asyncio.run(main())