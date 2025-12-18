# Implementation Plan: Workflow Data Model Integration

**Branch**: `001-workflow-data-model` | **Date**: Thu Dec 18 2025 | **Spec**: [specs/001-workflow-data-model/spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-workflow-data-model/spec.md`

## Summary

This feature integrates the existing workflow domain objects (Definition, Node, Edge) with the project's data schema management system to support "Configuration as Code". The primary goal is to enable **YAML-based persistence** of workflow definitions, allowing them to be versioned in Git alongside application code. This involves refactoring models for serialization compatibility, implementing strict schema validation (via Pydantic), and creating a file-based repository system for loading/saving workflows from `src/definitions/workflows`.

## Technical Context

**Language/Version**: Python 3.12 (inferred from `pyproject.toml` and modern tooling)
**Primary Dependencies**:
- **Pydantic**: For data modeling and schema validation.
- **PyYAML/Ruamel.yaml**: For YAML serialization/deserialization (specifically using `src.data.storage.YAMLStorage` wrapper).
- **Dolt/SQLAlchemy**: (Existing stack) Likely used for underlying data management, but this feature focuses on YAML layer.
**Storage**: File system (YAML files in `src/definitions/workflows`).
**Testing**: `pytest` for unit and integration testing.
**Target Platform**: Local development and server environments (cross-platform python).
**Project Type**: Single python project (libraries + CLI).
**Performance Goals**: Loading workflows should be sub-second; schema validation must be strict and immediate.
**Constraints**:
- Must leverage `src/data` capabilities (avoid reinventing schema wheels).
- Strict global uniqueness for Workflow IDs.
- Deterministic YAML output for clean git diffs.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Analysis

- **Library-First**: *Pass*. The workflow definitions will be part of the `src` module structure, effectively acting as a data library.
- **CLI Interface**: *Pass*. While primarily a data feature, the loading/validation will be accessible via standard script/CLI entry points (e.g., for seeding or validation).
- **Test-First**: *Pass*. Plan explicitly requires tests for serialization and validation before implementation.
- **Integration Testing**: *Pass*. "Round-trip" integration tests (YAML -> Object -> YAML) are a core success criterion.
- **Simplicity**: *Pass*. Using simple YAML files for configuration is a standard, low-complexity pattern compared to custom database loaders for static config.

**Evaluation**: The plan aligns with all core principles. No complex architectural deviations are proposed.

## Project Structure

### Documentation (this feature)

```text
specs/001-workflow-data-model/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (empty)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/
├── data/                    # Existing data schema capabilities (reused)
├── definitions/
│   └── workflows/           # NEW: Directory for YAML workflow files
├── models/
│   └── workflow/            # Existing domain models (refactored)
│       └── registry.py      # NEW: Workflow registry implementation
└── scripts/                 # Utility scripts (seed/validate)

tests/
├── data/
└── models/
    └── workflow/            # Unit tests for new serialization logic
```

**Structure Decision**: We will introduce `src/definitions/workflows` as the canonical store for YAML configurations. We will refactor `src/models/workflow` in place to support the new data schema mixins/bases from `src/data` and add a dedicated `registry.py` for loading.

## Complexity Tracking

*No violations found.*
