"""Workflow orchestrator for distributed expression evaluation."""

import logging
from datetime import timedelta

from temporalio import workflow

from .enums import Operator
from .exceptions import ParseError
from .models import ASTNode
from .parser import ExpressionParser

logger = logging.getLogger(__name__)


@workflow.defn
class EvaluateExpressionWorkflow:
    """Workflow that orchestrates distributed evaluation of math expressions."""

    # Map operators to their task queue and activity name
    OPERATOR_CONFIG = {
        Operator.ADD: {"task_queue": "queue-add", "activity": "add"},
        Operator.SUB: {"task_queue": "queue-sub", "activity": "subtract"},
        Operator.MUL: {"task_queue": "queue-mul", "activity": "multiply"},
        Operator.DIV: {"task_queue": "queue-div", "activity": "divide"},
        Operator.POW: {"task_queue": "queue-pow", "activity": "power"},
    }

    @workflow.run
    async def run(self, expression: str) -> float:
        """Execute the workflow.

        Parses the expression into an AST and dispatches activities to operator
        workers based on mathematical precedence and associativity rules.

        Args:
            expression: Mathematical expression string to evaluate

        Returns:
            The computed result as a float

        Raises:
            ParseError: If expression parsing fails
        """
        logger.info(f"Starting workflow for expression: {expression}")

        try:
            parser = ExpressionParser(expression)
            ast = parser.parse()
            logger.debug(f"Successfully parsed AST: {ast}")
        except ParseError as e:
            logger.error(f"Parse error: {str(e)}")
            raise

        result = await self._evaluate_ast(ast)
        logger.info(f"Workflow completed with result: {result}")
        return result

    async def _evaluate_ast(self, root: ASTNode) -> float:
        """Iteratively evaluate AST using post-order traversal.

        Two-pass approach:
        1. Build execution order (post-order, no recursion)
        2. Execute activities in that order

        Args:
            root: Root node of the AST

        Returns:
            The computed result
        """
        # Pass 1: Build execution order (iterative post-order traversal)
        execution_order = self._build_execution_order(root)

        # Pass 2: Execute activities in order
        results = {}

        for node in execution_order:
            if node.type == "number":
                # Store number values directly
                results[id(node)] = node.value
            else:
                # Get children values
                left_val = results[id(node.left)]
                right_val = results[id(node.right)]

                # Dispatch activity to operator worker
                result = await self._dispatch_activity(node.operator, left_val, right_val)
                results[id(node)] = result

        return results[id(root)]

    def _build_execution_order(self, root: ASTNode) -> list[ASTNode]:
        """Build post-order execution list using iterative stack traversal.

        Post-order: left -> right -> root
        This ensures children are processed before their parents.

        Args:
            root: Root node of the AST

        Returns:
            List of nodes in execution order
        """
        if root.type == "number":
            return [root]

        order = []
        # Stack holds (node, children_visited_flag)
        stack: list[tuple[ASTNode, bool]] = [(root, False)]

        while stack:
            node, children_done = stack.pop()

            if node.type == "number":
                order.append(node)
            elif children_done:
                # Both children processed, now process this node
                order.append(node)
            else:
                # First visit: push node back with flag, then push children
                stack.append((node, True))

                # Push right first, then left (so left is processed first)
                if node.right:
                    stack.append((node.right, False))
                if node.left:
                    stack.append((node.left, False))

        return order

    async def _dispatch_activity(self, operator: str, a: float, b: float) -> float:
        """Dispatch activity to the appropriate task queue.

        Args:
            operator: Operator symbol (+, -, *, /, ^)
            a: First operand
            b: Second operand

        Returns:
            Result of the operation
        """
        op = Operator(operator)
        config = self.OPERATOR_CONFIG[op]

        return await workflow.execute_activity(
            config["activity"],
            args=[a, b],
            task_queue=config["task_queue"],
            start_to_close_timeout=timedelta(seconds=30),
        )