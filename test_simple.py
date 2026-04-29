"""Test that submits expressions to the Temporal workflow queue."""

import asyncio
import logging

from temporalio.client import Client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def submit_expression(client: Client, expression: str) -> float:
    """Submit an expression to the workflow queue.

    Args:
        client: Temporal client
        expression: Math expression to evaluate

    Returns:
        The computed result
    """
    logger.info(f"Submitting expression to workflow: {expression}")

    try:
        result = await client.execute_workflow(
            "EvaluateExpressionWorkflow",
            expression,
            id=f"calc-{hash(expression) % 100000}",
            task_queue="queue-workflow",
        )
        logger.info(f"Result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise


async def main() -> None:
    """Connect to Temporal and submit test expressions."""
    try:
        # Connect to Temporal server
        client = await Client.connect("localhost:7233", namespace="calc")
        logger.info("Connected to Temporal server")

        # Test expressions
        test_cases = [
            ("1 + 5^3 * (2 - 5)", -374.0),
            ("10 + 5", 15.0),
            ("2 * 3 + 4", 10.0),
            ("10 / 2", 5.0),
            ("2 ^ 3", 8.0),
            ("(1 + 2) * 3", 9.0),
            ("100 - 50 / 2", 75.0),
        ]

        passed = 0
        failed = 0

        for expression, expected in test_cases:
            try:
                result = await submit_expression(client, expression)
                if result == expected:
                    logger.info(f"✓ PASSED: {expression} = {result}\n")
                    passed += 1
                else:
                    logger.error(f"✗ FAILED: {expression} = {result}, expected {expected}\n")
                    failed += 1
            except Exception as e:
                logger.error(f"✗ FAILED: {expression} - {str(e)}\n")
                failed += 1

        logger.info(f"\n{'='*50}")
        logger.info(f"Results: {passed} passed, {failed} failed")
        logger.info(f"{'='*50}")

        # Note: Client doesn't need explicit close in newer versions

    except Exception as e:
        logger.error(f"Failed to connect to Temporal: {str(e)}")
        logger.error("Make sure Temporal server is running on localhost:7233")


if __name__ == "__main__":
    asyncio.run(main())
