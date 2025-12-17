# System Catalyst

System Catalyst is an opinionated framework for building digital systems tailored to your custom use cases. It enables rapid, incremental development while enforcing strict architectural principles to ensure long-term maintainability and scalability.

## Core Philosophy

System Catalyst is built on a foundation of strict **Model-View-Controller (MVC)** separation of concerns. By enforcing clear boundaries between data, business logic, and user interface, the framework ensures that systems remain modular, testable, and adaptable to change.

## Architecture & Tech Stack

System Catalyst orchestrates a modern Python stack to deliver a cohesive development experience:

### Model Layer (Data & State)
*   **Version Control First:** We treat data with the same rigor as code.
    *   **Database:** [Dolt](https://www.dolthub.com/) is used as the primary RDBMS, providing Git-like version control for your SQL database.
    *   **File System:** Git is used for version-controlled file management.
*   **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) for robust database interactions.
*   **Validation:** [Pydantic](https://docs.pydantic.dev/) for strict data modeling and validation.

### Control Layer (Business Logic)
*   **API:** [FastAPI](https://fastapi.tiangolo.com/) exposes business logic via RESTful endpoints.
*   **Logic:** Pure Python implementations encapsulate core business rules, completely decoupled from the UI.

### View Layer (User Interface)
*   **UI Framework:** [Flet](https://flet.dev/) allows for the rapid construction of consistent, responsive interfaces that run on both desktop and web platforms from a single Python codebase.

## Getting Started

### Prerequisites
*   Python 3.12+
*   [uv](https://github.com/astral-sh/uv) for fast Python package and project management.

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/systemcatalyst.git
    cd systemcatalyst
    ```

2.  Install dependencies:
    ```bash
    uv sync
    ```

### Development

*   **Run UI:** `uv run flet run src/ui/main.py`
*   **Run Service:** `uv run uvicorn src.service.main:app --reload`
*   **Run Tests:** `uv run pytest`

*   **Lint:** `uv run ruff check .`
*   **Format:** `uv run ruff format .`
*   **Documentation:** `uv run mkdocs serve`

For detailed developer guidelines, please refer to [AGENTS.md](AGENTS.md).

### Data Definition to SQL

You can now use this method to drive the generation process safely:
1. Load Registry
```python
registry.load_from_directory(...)
```
2. Get safe creation order
```python
try:
    ordered_tables = registry.get_ordered_schemas()
except ValueError as e:
    print(f"Cannot generate schema: {e}")
    exit(1)
```
3. Generate DDL
```python
generator.generate_ddl(ordered_tables)
```

## License

[MIT License](LICENSE)
