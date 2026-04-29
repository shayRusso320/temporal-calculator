"""Pydantic models for the distributed calculator system."""

from pydantic import BaseModel, Field


class ASTNode(BaseModel):
    """Represents a node in the Abstract Syntax Tree."""

    type: str = Field(..., description="Type of node: 'number' or 'operator'")
    value: float | None = Field(None, description="Numeric value if type is 'number'")
    operator: str | None = Field(None, description="Operator symbol if type is 'operator'")
    left: "ASTNode | None" = Field(None, description="Left child node")
    right: "ASTNode | None" = Field(None, description="Right child node")


ASTNode.model_rebuild()


class EvaluationResult(BaseModel):
    """Result of expression evaluation."""

    result: float = Field(..., description="The computed result")
    expression: str = Field(..., description="The original expression")
