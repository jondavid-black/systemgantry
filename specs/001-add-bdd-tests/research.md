# Research Findings - Add BDD Testing

**Feature**: Add BDD Testing
**Branch**: `001-add-bdd-tests`

## Decisions

### 1. Test Framework
- **Decision**: Use `behave` for BDD testing.
- **Rationale**: User explicitly requested `behave`. It is the industry standard for Python BDD.
- **Alternatives Considered**: `pytest-bdd` (discarded per requirement).

### 2. YAML Handling
- **Decision**: Use `ruamel.yaml` instead of `PyYAML`.
- **Rationale**: Research confirmed `ruamel.yaml` is already a project dependency in `pyproject.toml`. It offers better YAML spec compliance and round-trip capabilities.
- **Alternatives Considered**: Adding `PyYAML` as a new dependency (redundant).

### 3. ProtoBuf Verification
- **Decision**: String-based comparison for ProtoBuf export tests.
- **Rationale**: The existing `ProtobufGenerator` implementation uses string generation/templating. Tests should verify the generated string output against expected `.proto` file content (golden files or inline strings). Using `grpcio-tools` to compile the generated output could be a secondary validation step but simple string comparison is sufficient for the initial acceptance criteria.

### 4. Integration with Existing Code
- **Decision**: BDD steps will import and usage `src.data.registry.SchemaRegistry` and `src.data.generator.SchemaGenerator` directly.
- **Rationale**: The core logic already exists in `src/data/`. The BDD tests will act as high-level integration tests wrapping these classes.

## Unknowns Resolved

- **[NEEDS CLARIFICATION: confirm-existing-codebase-state]**: Resolved. `SchemaRegistry`, `SchemaGenerator` (SQL), and `ProtobufGenerator` (ProtoBuf) all exist and have unit tests. The BDD tests will add a layer of acceptance testing on top.
- **[NEEDS CLARIFICATION: proto-export-method]**: Resolved. Implemented via manual string generation in `src/data/generator.py`.
