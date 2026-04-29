"""Enums for the distributed calculator system."""

from enum import Enum


class Operator(str, Enum):
    """Supported arithmetic operators."""

    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    POW = "^"
