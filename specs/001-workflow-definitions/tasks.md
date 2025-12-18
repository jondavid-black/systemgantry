# Tasks: Workflow Definitions

**Feature**: Workflow Definitions
**Status**: PENDING
**Plan**: [plan.md](./plan.md)

## Phase 1: Setup

*Goal: Initialize the project structure for the new feature models.*

- [x] T001 [P] Create directory structure for workflow models in `src/models/workflow`
- [x] T002 [P] Create `__init__.py` in `src/models/workflow` to export models
- [x] T003 Create `src/scripts` directory if not exists (for seed script)

## Phase 2: Foundational

*Goal: Implement the core shared components required for all User Stories.*

- [x] T004 Define `WorkflowNodeType` Enum in `src/models/workflow/enums.py`
- [x] T005 [P] Implement `WorkflowEdge` Pydantic model in `src/models/workflow/edge.py`
- [x] T006 Implement Property Models (`ProcessProps`, `TriggerProps`, `EmptyProps`) in `src/models/workflow/properties.py`
- [x] T007 [P] Implement base `WorkflowNode` class in `src/models/workflow/node.py`

## Phase 3: User Story 1 - Define Workflow Data Structure (P1)

*Goal: Define the structure of a workflow using various block types so that I can map out complex business logic.*

**Independent Test**: Run `seed_workflow.py` to instantiate models with all block types and verify structure.

- [x] T008 [US1] Implement `ProcessNode` and `TriggerNode` models in `src/models/workflow/node.py`
- [x] T009 [US1] Implement `DecisionNode`, `BranchNode`, `JoinNode`, `CompletionNode` in `src/models/workflow/node.py`
- [x] T010 [US1] Implement `WorkflowDefinition` aggregate model in `src/models/workflow/definition.py`
- [x] T011 [US1] Implement `WorkflowNode` union type/discriminator in `src/models/workflow/node.py`
- [x] T012 [P] [US1] Implement `validate_workflow` function (Cycle/Island detection) in `src/models/workflow/validation.py`
- [x] T013 [US1] Create `src/scripts/seed_workflow.py` to instantiate and print a complex workflow
- [x] T014 [US1] Add SQL Alchemy mapping (STI) for `WorkflowNode` in `src/models/workflow/sql.py` (if required by project, or stick to Pydantic for now as per plan "Models only")
- [x] T015 [US2] Ensure `WorkflowDefinition` has `use_case_id` field in `src/models/workflow/definition.py`
- [x] T016 [P] [US2] Update `seed_workflow.py` to include a test case with `use_case_id`
- [x] T017 [US2] Update `validate_workflow` in `src/models/workflow/validation.py` to warn if `use_case_id` is missing (optional strictness check)

## Final Phase: Polish

*Goal: Ensure code quality, consistency, and documentation.*

- [x] T018 Run `ruff check .` and fix any linting errors in `src/models/workflow`
- [x] T019 Update `quickstart.md` with output from the final `seed_workflow.py` run
- [x] T020 Verify all imports in `src/models/workflow/__init__.py` are correct

## Dependencies

1. T001-T003 (Setup) -> T004-T007 (Foundational)
2. T004-T007 -> T008-T011 (US1 Core Models)
3. T008-T011 -> T012 (Validation), T013 (Seed Script)
4. T010 -> T015 (US2 Field)

## Implementation Strategy

1. **MVP Scope**: Focus on getting the Pydantic models (T008-T011) and the Seed Script (T013) working first. This proves the data structure.
2. **Validation**: Add the custom DFS/BFS logic (T012) after the structure is proven.
3. **Traceability**: `use_case_id` is a simple field add, can be done anytime, but logically fits after the core structure.
