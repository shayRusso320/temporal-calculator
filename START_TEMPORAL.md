# Starting Temporal Server

## Option 1: Using Temporal CLI (Recommended)

Install Temporal CLI:
```bash
# On Windows with Chocolatey
choco install temporal-cli

# Or download from: https://github.com/temporalio/cli/releases
```

Start the server:
```bash
temporal server start-dev
```

This starts Temporal on `localhost:7233` with UI on `http://localhost:8080`

## Option 2: Using Docker

```bash
docker run -d --name temporal -p 7233:7233 -p 6233:6233 temporaliotest/auto-setup:latest
```

## Option 3: Build from Source

```bash
git clone https://github.com/temporalio/temporal.git
cd temporal
make build
./temporal server start-dev
```

Once the server is running, you can:
1. Run the workers: `python -m src.operators.add.main` etc.
2. Run the test: `python test_simple.py`
3. View the UI: http://localhost:8080
