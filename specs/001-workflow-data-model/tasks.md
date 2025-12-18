---
description: "Task list for Workflow Data Model Integration"
---

# Tasks: Workflow Data Model Integration

**Input**: Design documents from `/specs/001-workflow-data-model/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are explicitly requested in the specification ("Test-First" principle).
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create directory `src/definitions/workflows` for YAML storage
- [ ] T002 Create directory `src/models/workflow` if not exists (should exist)
- [ ] T003 Create directory `tests/models/workflow` for new tests

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Implement `WorkflowRegistry` class in `src/models/workflow/registry.py` (empty class skeleton)
- [ ] T005 [P] Create empty `__init__.py` in `src/definitions/workflows`
- [ ] T006 [P] Create `validate_workflows.py` script skeleton in `src/scripts/`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - YAML-Based Workflow Management (Priority: P1) 🎯 MVP

**Goal**: Enable defining and managing workflow definitions as YAML files for version control.

**Independent Test**: Create a workflow definition YAML file in `src/definitions/workflows`, load it into the application, and verify the in-memory object graph matches the file definition.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T007 [US1] Create unit test for loading valid YAML in `tests/models/workflow/test_registry_loading.py`
- [ ] T008 [US1] Create unit test for round-trip serialization in `tests/models/workflow/test_serialization.py`

### Implementation for User Story 1

- [ ] T009 [US1] Refactor `WorkflowDefinition`, `Node`, `Edge` in `src/models/workflow/` to support `YAMLStorage` serialization (ensure Pydantic compatibility)
- [ ] T010 [US1] Implement `load_from_directory` method in `src/models/workflow/registry.py` using `src.data.storage.YAMLStorage`
- [ ] T011 [US1] Implement `get_workflow` method in `src/models/workflow/registry.py`
- [ ] T012 [US1] Update `src/scripts/seed_workflow.py` to use `YAMLStorage` for saving workflows

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Schema Validation (Priority: P1)

**Goal**: Validate workflow YAML files against a strict schema to prevent runtime errors.

**Independent Test**: Create a YAML file with intentional errors (e.g., missing required 'id' field), attempt to load it, and verify the system reports a validation error.

### Tests for User Story 2 ⚠️

- [ ] T013 [US2] Create unit test for missing required fields in `tests/models/workflow/test_validation.py`
- [ ] T014 [US2] Create unit test for duplicate IDs in `tests/models/workflow/test_validation.py`
- [ ] T015 [US2] Create unit test for invalid edge references in `tests/models/workflow/test_validation.py`

### Implementation for User Story 2

- [ ] T016 [US2] Add strict uniqueness check in `src/models/workflow/registry.py` during loading
- [ ] T017 [US2] Update `src/models/workflow/validation.py` to support deep validation (graph connectivity)
- [ ] T018 [US2] Implement validation logic in `src/scripts/validate_workflows.py`
- [ ] T019 [US2] Ensure `WorkflowDefinition` model enforces Pydantic constraints for all fields

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T020 [P] Update documentation in `docs/` to reflect new YAML workflow process
- [ ] T021 Run `quickstart.md` steps to verify end-to-end flow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Ideally after US1 data structures are settled, but can run in parallel if models are stable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints/scripts
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Tests for US1 and US2 can be written in parallel
- Implementation of US1 models and US2 validation logic can overlap if coordination exists

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Create unit test for loading valid YAML in tests/models/workflow/test_registry_loading.py"
Task: "Create unit test for round-trip serialization in tests/models/workflow/test_serialization.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories
