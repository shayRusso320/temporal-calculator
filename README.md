# Distributed Calculator with Temporal

A distributed arithmetic expression evaluator using Temporal workflows. Each operator type runs in its own worker process.

## Project Structure

```
src/
├── operators/
│   ├── add/          # Addition operator worker
│   ├── subtract/     # Subtraction operator worker
│   ├── multiply/     # Multiplication operator worker
│   ├── divide/       # Division operator worker
│   └── power/        # Power/exponentiation operator worker
├── workflow/         # Workflow orchestrator
├── parser.py         # Expression parser (builds AST)
├── models.py         # Pydantic data models
├── exceptions.py     # Custom exceptions
├── config.py         # Configuration management
├── enums.py          # Operator enums
└── client.py         # Client for submitting expressions
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install from individual operator requirements:

```bash
pip install -r src/operators/add/requirements.txt
```

### 2. Start Temporal Server

Using Docker Compose:

```bash
docker-compose up -d
```

This starts:
- Temporal server on `localhost:7233`
- Temporal UI on `http://localhost:8080`

### 3. Start Workers

Start each worker in a separate terminal:

```bash
# Terminal 1 - Addition operator
python -m src.operators.add.main

# Terminal 2 - Subtraction operator
python -m src.operators.subtract.main

# Terminal 3 - Multiplication operator
python -m src.operators.multiply.main

# Terminal 4 - Division operator
python -m src.operators.divide.main

# Terminal 5 - Power operator
python -m src.operators.power.main

# Terminal 6 - Workflow orchestrator
python -m src.workflow.main
```

## Testing

Run the test script to evaluate expressions:

```bash
python test_calculator.py
```

### Example Expressions

The test script evaluates:
- `1 + 5^3 * (2 - 5)` → `-374`
- `10 + 5` → `15`
- `2 * 3 + 4` → `10`
- `10 / 2` → `5.0`
- `2 ^ 3` → `8.0`
- `(1 + 2) * 3` → `9.0`
- `100 - 50 / 2` → `75.0`

## How It Works

1. **Parser**: Converts the expression string into an Abstract Syntax Tree (AST) respecting operator precedence and associativity
2. **Workflow**: Orchestrates the evaluation by recursively walking the AST
3. **Activities**: Each operator dispatches an activity to its dedicated task queue
4. **Workers**: Operator workers listen on their task queues and execute activities
5. **Results**: Activities return computed values which bubble up the AST

### Operator Precedence

- `^` (power) - highest, right-associative
- `*` `/` (multiply, divide) - medium, left-associative
- `+` `-` (add, subtract) - lowest, left-associative

### Task Queues

| Operator | Task Queue |
|----------|-----------|
| `+` | `queue-add` |
| `-` | `queue-sub` |
| `*` | `queue-mul` |
| `/` | `queue-div` |
| `^` | `queue-pow` |
| Workflow | `queue-workflow` |

## Configuration

Set environment variables in `.env`:

```env
TEMPORAL_HOST=localhost
TEMPORAL_PORT=7233
TEMPORAL_NAMESPACE=default
```

## Error Handling

- **Division by zero**: Raises `DivisionByZeroError`
- **Invalid expressions**: Raises `ParseError` before any activities are dispatched
- **Activity failures**: Temporal surfaces them as workflow failures with retry policy
