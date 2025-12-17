---
description: "Task list for adding BDD testing with behave"
---

# Tasks: Add BDD Testing

**Input**: Design documents from `/specs/001-add-bdd-tests/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are the primary deliverable of this feature, so test tasks are explicit implementation steps.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Add `behave` to dev dependencies using `uv add --dev behave`
- [x] T002 Create `features/` directory structure with `steps/` and `data/` subdirectories
- [x] T003 [P] Create `features/environment.py` with basic before/after hooks
- [x] T004 [P] Create `features/steps/common_steps.py` for shared step definitions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create `features/data/valid_schema.yaml` with sample schema content (User/Post models) for testing
- [x] T006 [P] Create `features/data/expected_sql.txt` and `features/data/expected_proto.txt` with expected output templates
- [x] T007 [P] Create `features/steps/registry_steps.py` skeleton for registry interaction steps
- [x] T008 [P] Create `features/steps/export_steps.py` skeleton for export verification steps

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Enable BDD Testing Infrastructure (Priority: P1) 🎯 MVP

**Goal**: Configure project with BDD framework to write and execute acceptance tests

**Independent Test**: Verify `behave` is installed and runs a trivial feature file

### Implementation for User Story 1

- [x] T009 [US1] Create `features/infrastructure.feature` with scenarios to check dependency installation and directory structure
- [x] T010 [US1] Implement steps in `features/steps/infrastructure_steps.py` to verify `behave` dependency presence
- [x] T011 [US1] Implement steps in `features/steps/infrastructure_steps.py` to verify `features/` directory existence
- [x] T012 [US1] Run `uv run behave features/infrastructure.feature` to verify infrastructure setup

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Verify YAML to SQL Transformation (Priority: P2)

**Goal**: Verify valid YAML schema definitions are loaded and exported as SQL

**Independent Test**: Run `features/sql_export.feature` and assert output matches expected SQL DDL

### Implementation for User Story 2

- [x] T013 [US2] Create `features/sql_export.feature` with scenarios for loading YAML and exporting SQL
- [x] T014 [US2] Implement "Given a valid YAML schema definition file" step in `features/steps/registry_steps.py` (loads `features/data/valid_schema.yaml`)
- [x] T015 [US2] Implement "Then the registry should contain the defined schema entities" step in `features/steps/registry_steps.py`
- [x] T016 [US2] Implement "When I request an SQL export" step in `features/steps/export_steps.py` using `src.data.generator.SchemaGenerator`
- [x] T017 [US2] Implement "Then the system should generate valid SQL DDL statements" step in `features/steps/export_steps.py` (compares against `features/data/expected_sql.txt`)
- [x] T018 [US2] Run `uv run behave features/sql_export.feature` to verify SQL export logic

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Verify YAML to Protocol Buffers Transformation (Priority: P2)

**Goal**: Verify valid YAML schema definitions are loaded and exported as Protocol Buffers

**Independent Test**: Run `features/proto_export.feature` and assert output matches expected .proto syntax

### Implementation for User Story 3

- [x] T019 [US3] Create `features/proto_export.feature` with scenarios for loading YAML and exporting ProtoBuf
- [x] T020 [US3] Implement "When I request a ProtoBuf export" step in `features/steps/export_steps.py` using `src.data.generator.ProtobufGenerator`
- [x] T021 [US3] Implement "Then the system should generate valid Protocol Buffer definitions" step in `features/steps/export_steps.py` (compares against `features/data/expected_proto.txt`)
- [x] T022 [US3] Run `uv run behave features/proto_export.feature` to verify ProtoBuf export logic

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T023 [P] Update `docs/quickstart.md` with instructions for running BDD tests
- [x] T024 Verify all BDD tests run successfully with `uv run behave`
- [x] T025 Add CI workflow step to run BDD tests (if CI file exists/accessible)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Relies on shared steps but implementation is independent
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Relies on shared steps but implementation is independent

### Parallel Opportunities

- T003 (`environment.py`) and T004 (`common_steps.py`) can run in parallel
- T006 (`registry_steps.py`) and T007 (`export_steps.py`) can run in parallel
- Once Foundational phase is done, User Story 2 and User Story 3 can technically be implemented in parallel as they touch different feature files and step functions

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Run `behave features/infrastructure.feature`
5. Demonstrate working test runner

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Verify infrastructure → MVP!
3. Add User Story 2 → Verify SQL export logic
4. Add User Story 3 → Verify ProtoBuf export logic
5. Run full suite → All green
