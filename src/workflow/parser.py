"""Expression parser for the distributed calculator system."""

import logging
import re

from .enums import Operator
from .exceptions import ParseError
from .models import ASTNode

logger = logging.getLogger(__name__)


class ExpressionParser:
    """Parses mathematical expressions into Abstract Syntax Trees."""

    def __init__(self, expression: str):
        """Initialize parser with expression string.

        Args:
            expression: Mathematical expression to parse

        Raises:
            ParseError: If expression is empty or invalid
        """
        self.expression = expression.strip()
        self.pos = 0
        if not self.expression:
            raise ParseError("Expression cannot be empty")
        logger.debug(f"Initialized parser with expression: {self.expression}")

    def parse(self) -> ASTNode:
        """Parse expression into AST.

        Returns:
            Root node of the Abstract Syntax Tree

        Raises:
            ParseError: If expression is invalid
        """
        try:
            node = self._parse_addition()
            if self.pos < len(self.expression):
                raise ParseError(f"Unexpected character at position {self.pos}")
            logger.debug("Successfully parsed expression into AST")
            return node
        except ParseError:
            raise
        except Exception as e:
            raise ParseError(f"Parse error: {str(e)}")

    def _parse_addition(self) -> ASTNode:
        """Parse addition and subtraction (lowest precedence).

        Returns:
            AST node for addition/subtraction expression
        """
        left = self._parse_multiplication()

        while self.pos < len(self.expression):
            self._skip_whitespace()
            if self.pos >= len(self.expression):
                break
            if self.expression[self.pos] in ("+", "-"):
                op = self.expression[self.pos]
                self.pos += 1
                right = self._parse_multiplication()
                left = ASTNode(
                    type="operator",
                    operator=op,
                    left=left,
                    right=right,
                )
            else:
                break

        return left

    def _parse_multiplication(self) -> ASTNode:
        """Parse multiplication and division (medium precedence).

        Returns:
            AST node for multiplication/division expression
        """
        left = self._parse_power()

        while self.pos < len(self.expression):
            self._skip_whitespace()
            if self.pos >= len(self.expression):
                break
            if self.expression[self.pos] in ("*", "/"):
                op = self.expression[self.pos]
                self.pos += 1
                right = self._parse_power()
                left = ASTNode(
                    type="operator",
                    operator=op,
                    left=left,
                    right=right,
                )
            else:
                break

        return left

    def _parse_power(self) -> ASTNode:
        """Parse exponentiation (highest precedence, right-associative).

        Returns:
            AST node for power expression
        """
        left = self._parse_unary()

        self._skip_whitespace()
        if self.pos < len(self.expression) and self.expression[self.pos] == "^":
            self.pos += 1
            right = self._parse_power()  # Right-associative recursion
            return ASTNode(
                type="operator",
                operator="^",
                left=left,
                right=right,
            )

        return left

    def _parse_unary(self) -> ASTNode:
        """Parse unary operators and primary expressions.

        Returns:
            AST node for unary or primary expression
        """
        self._skip_whitespace()

        if self.pos < len(self.expression) and self.expression[self.pos] == "-":
            self.pos += 1
            operand = self._parse_unary()
            # Represent unary minus as 0 - operand
            return ASTNode(
                type="operator",
                operator="-",
                left=ASTNode(type="number", value=0.0),
                right=operand,
            )

        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        """Parse primary expressions (numbers and parenthesized expressions).

        Returns:
            AST node for primary expression

        Raises:
            ParseError: If primary expression is invalid
        """
        self._skip_whitespace()

        if self.pos >= len(self.expression):
            raise ParseError("Unexpected end of expression")

        if self.expression[self.pos] == "(":
            self.pos += 1
            node = self._parse_addition()
            self._skip_whitespace()
            if self.pos >= len(self.expression) or self.expression[self.pos] != ")":
                raise ParseError("Missing closing parenthesis")
            self.pos += 1
            return node

        return self._parse_number()

    def _parse_number(self) -> ASTNode:
        """Parse numeric literal.

        Returns:
            AST node with numeric value

        Raises:
            ParseError: If number format is invalid
        """
        self._skip_whitespace()

        match = re.match(r"(\d+\.?\d*|\.\d+)", self.expression[self.pos :])
        if not match:
            raise ParseError(f"Invalid number at position {self.pos}")

        num_str = match.group(0)
        self.pos += len(num_str)
        value = float(num_str)

        return ASTNode(type="number", value=value)

    def _skip_whitespace(self) -> None:
        """Skip whitespace characters."""
        while self.pos < len(self.expression) and self.expression[self.pos].isspace():
            self.pos += 1
