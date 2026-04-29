"""Power operator worker."""

import asyncio
import logging

from temporalio import activity
from temporal_worker_sdk import TemporalSDK

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@activity.defn
async def power(a: float, b: float) -> float:
    """Raise a to the power of b."""
    return a**b


async def main():
    sdk = TemporalSDK()
    sdk.register_activities(power)
    await sdk.start()


if __name__ == "__main__":
    asyncio.run(main())
