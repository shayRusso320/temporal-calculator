"""Power operator worker."""

import asyncio
import logging

from temporal_worker_sdk import TemporalSDK

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def power(a: float, b: float) -> float:
    """Raise a to the power of b."""
    return a**b


async def main():
    sdk = TemporalSDK()
    sdk.register_activities(add)
    await sdk.start()


if __name__ == "__main__":
    asyncio.run(main())
