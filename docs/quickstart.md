# Quickstart

## Prerequisites
- Python 3.x
- `uv` package manager

## Installation

1. Install development dependencies:
   ```bash
   uv sync --dev
   ```

## Running BDD Tests

1. Execute the full BDD suite:
   ```bash
   uv run behave
   ```

2. Run a specific feature:
   ```bash
   uv run behave features/sql_export.feature
   ```

3. Run with WIP (Work In Progress) tag:
   ```bash
   uv run behave -t @wip
   ```

## Adding New Tests

1. Create a new `.feature` file in `features/`.
2. Define scenarios using Gherkin syntax.
3. If new steps are needed, implement them in `features/steps/`.
4. Run `uv run behave` to verify.

## Running Unit Tests
To run the existing unit tests:
```bash
uv run pytest
```
