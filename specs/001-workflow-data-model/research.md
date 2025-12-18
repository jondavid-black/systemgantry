# Research Phase: Workflow Data Model Integration

**Branch**: `001-workflow-data-model` | **Date**: Thu Dec 18 2025

## 1. Decisions & Findings

### Decision 1: Leverage `src.data.storage.YAMLStorage`
**Decision**: Use existing `YAMLStorage` class for low-level file I/O.
**Rationale**: It provides consistent YAML handling (using `ruamel.yaml`) across the project, supporting round-trip capabilities (comments preservation).
**Alternatives Considered**:
- *Custom PyYAML implementation*: Rejected to avoid duplicating YAML configuration logic and inconsistent formatting.

### Decision 2: Create Dedicated `WorkflowRegistry`
**Decision**: Implement a new `WorkflowRegistry` in `src/models/workflow/registry.py` mirroring `src/data/registry.py`.
**Rationale**: The existing `SchemaRegistry` is tightly coupled to `TableSchema` objects. Workflows are distinct domain entities. Following the pattern (load from directory, validate, cache) is better than forcing inheritance.
**Alternatives Considered**:
- *Generic Registry*: Attempting to make `SchemaRegistry` generic. Rejected as it would require refactoring the core data layer which is out of scope and risky.

### Decision 3: Pydantic for Data Model
**Decision**: Continue using Pydantic models for `WorkflowDefinition`, `Node`, and `Edge`.
**Rationale**: Models already inherit from `BaseModel`. This aligns perfectly with the requirement for strict schema validation.
**Unknowns Resolved**: Confirmed that `src/models/workflow` classes are already Pydantic models, not plain classes.

## 2. Unknowns Resolution

| Unknown | Status | Resolution |
|---------|--------|------------|
| `src/data` serialization base | **Resolved** | No base class; relies on Pydantic + `src/data/storage.py` utility. |
| Registry mechanism | **Resolved** | `SchemaRegistry` exists but is specific. Pattern should be copied/adapted. |
| Workflow model state | **Resolved** | Already Pydantic models. Need to ensure polymorphic loading works with `YAMLStorage` dict output. |

## 3. Best Practices (Validation)

- **Polymorphism**: Ensure `WorkflowDefinition.nodes` uses `Discriminator` or `Union` properly so Pydantic instantiates the correct node subclass (Trigger vs Process) from YAML data.
- **Uniqueness**: The registry must enforce unique IDs across all loaded files upon load.
- **Directory Scanning**: Use `pathlib` for robust recursive directory scanning in the registry.
