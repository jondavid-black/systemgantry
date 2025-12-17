# AGENTS.md - Developer Guide

## Project Overview
System Catalyst is a framework for developing digital systems tailored to specific use cases, enabling rapid, incremental development while maintaining opinionated core system design principles. The project emphasizes strict Model-View-Controller (MVC) separation of concerns across all system layers.

## Architecture Principles

### Model Layer (Data Layer)
- Emphasizes version control and strict review of system baseline content
- Supports both database and file system content management
- **Database**: Dolt as the primary RDBMS (version-controlled database)
- **File System**: Git for version-controlled file management
- **ORM**: SQLAlchemy for database interactions
- **Validation**: Pydantic for data modeling and validation

### Control Layer (Business Logic)
- Python-based implementations exposed via FastAPI endpoints
- Interacts with Model layer using SQLAlchemy and Pydantic
- RESTful API design principles
- Business logic encapsulation and service layer patterns

### View Layer (User Interface)
- Flet for rapid development of consistent desktop and web interfaces
- Cross-platform UI development (desktop and web)
- Component-based design system
- Responsive and accessible interface patterns

## Project Type
Python project (greenfield - no source code yet)

## Environment Management
- Use `uv` for package management and virtual environment
- All commands should be run with `uv run` prefix

## Project Structure
- `src/` - Source code directory
  - `models/` - Model layer implementations (SQLAlchemy, Pydantic)
  - `controllers/` - Control layer (FastAPI endpoints, business logic)
  - `views/` - View layer (Flet UI components)
- `tests/` - Unit tests directory  
- `docs/` - Documentation directory
- `pyproject.toml` - Project configuration

## Build/Test Commands
- Tests: `uv run pytest` or `uv run pytest tests/`
- Single test: `uv run pytest tests/test_specific.py::TestClass::test_method`
- Linting: `uv run ruff check .`
- Formatting: `uv run ruff format .`
- Type Checking: `uv run pyright`
- Documentation: `uv run mkdocs serve` (dev) / `uv run mkdocs build` (prod)

## Code Style Guidelines
- Follow PEP 8 for naming (snake_case for functions/variables, PascalCase for classes)
- Use type hints for function parameters and return types
- Import order: standard library, third-party, local imports
- Use docstrings for modules, classes, and functions
- Handle errors with specific exceptions, not bare `except:`
- Use context managers (`with` statements) for resource management
- **MVC Separation**: Strict adherence to layer boundaries - no cross-layer imports
- **Data Flow**: View → Controller → Model → Controller → View

## Core Dependencies
- **Database**: Dolt (version-controlled RDBMS)
- **ORM**: SQLAlchemy
- **API**: FastAPI
- **Validation**: Pydantic
- **UI**: Flet
- **Testing**: pytest
- **Documentation**: mkdocs
- **Code Quality**: ruff (linting + formatting)
- **Version Control**: git (file system), Dolt (database)

## Development Guidelines
- Always maintain MVC separation - controllers should not import view components
- Models should be independent of both controllers and views
- Views should only interact with controllers, never directly with models
- Use Pydantic models for data validation and serialization between layers
- Implement proper error handling and logging at each layer
- Database changes should be version-controlled through Dolt
- All API endpoints should follow RESTful conventions
- UI components should be reusable and maintain consistency

## Notes
- .gitignore prepared for modern Python tooling (ruff, mypy, pytest, jupyter)
- No existing Cursor rules or Copilot instructions found
