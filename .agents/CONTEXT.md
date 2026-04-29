# Distributed Calculator — Mission Description

## Context

We are building a distributed arithmetic expression evaluator using Temporal workflows.
The system takes a math expression as a string input and evaluates it in a distributed way —
each operator type is handled by a dedicated worker process. The goal is to demonstrate
Temporal's orchestration capabilities, not to build an efficient calculator.

The Worker SDK is already built and available as a package. All workers in this system
use it to bootstrap themselves.

---

## How the System Works

### The Workflow Worker
The workflow worker is the brain of the system. It receives the raw expression string,
parses it into an AST (Abstract Syntax Tree), and orchestrates the evaluation by dispatching
activities to the appropriate operator workers. It holds all state and knows the full execution
plan. It does not perform any arithmetic itself.

### The Operator Workers
Each operator type has its own dedicated worker process listening on its own task queue.
Operator workers are completely dumb — they receive two numbers, perform one arithmetic
operation, and return one number. They know nothing about the original expression, the AST,
or what step they are in the evaluation.

### Task Queue Routing
| Operator | Task Queue |
|---|---|
| `+` | `queue-add` |
| `-` | `queue-sub` |
| `*` | `queue-mul` |
| `/` | `queue-div` |
| `^` | `queue-pow` |
| workflow | `queue-workflow` |

---

## Expression Parsing

The workflow worker parses the input string into an AST before dispatching any activities.
The parser must handle:

- Operators: `+` `-` `*` `/` `^`
- Parentheses for grouping
- Correct operator precedence: `^` then `*` `/` then `+` `-`
- Correct associativity: `^` is right-associative, all others are left-associative
- Integer and floating point numbers
- Negative numbers

No external parser libraries — implement from scratch.

---

## Evaluation Strategy

The workflow walks the AST bottom-up recursively. For each operator node:

1. Evaluate left and right child subtrees — in parallel if they are independent
2. Dispatch an activity to the correct task queue with the two resolved numbers
3. Wait for the result and pass it up the tree

Activities always receive exactly two floats and return exactly one float.

---

## What Each Operator Worker Looks Like

```python
from worker_sdk import WorkerSDK

sdk = WorkerSDK()

@sdk.activity
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

sdk.start()
```

All five operator workers follow this exact pattern. Only the function and TASK_QUEUE env var differ.

---

## Example Execution

Expression: `1 + 5^3 * (2 - 5)`
Step 1: pow(5, 3)      -> 125        dispatched to queue-pow
Step 2: sub(2, 5)      -> -3         dispatched to queue-sub  (parallel with step 1)
Step 3: mul(125, -3)   -> -375       dispatched to queue-mul
Step 4: add(1, -375)   -> -374       dispatched to queue-add

Expected result: -374

---

## Error Handling

- Division by zero: divide activity raises ValueError — Temporal surfaces it as workflow failure
- Invalid expression: parser raises before any activities are dispatched
- Activity failures: rely on workflow retry policy, no retry logic inside activities

---

## Non-Functional Requirements

- Each worker is a separate process and separate deployment
- No hardcoded values — all config via environment variables through the SDK
- All activity functions must have type hints
- Workflow must be deterministic — no randomness, no direct I/O, no system clock calls inside workflow code