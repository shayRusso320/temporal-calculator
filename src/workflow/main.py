"""Entry point for the workflow worker."""

import asyncio
import logging

from temporal_worker_sdk import TemporalSDK

from src.workflow.orchestrator import EvaluateExpressionWorkflow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


async def main():
    sdk = TemporalSDK()
    sdk.register_workflows(EvaluateExpressionWorkflow)
    await sdk.start()


if __name__ == "__main__":
    asyncio.run(main())