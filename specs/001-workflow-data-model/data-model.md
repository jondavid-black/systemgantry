# Data Model: Workflow Persistence

**Branch**: `001-workflow-data-model` | **Date**: Thu Dec 18 2025

## 1. Domain Entities

### `WorkflowDefinition`
The root aggregate for a workflow. Mapped to a single YAML file.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `str` | Yes | Unique identifier (snake_case). |
| `name` | `str` | Yes | Human-readable name. |
| `description` | `str` | No | Optional description. |
| `version` | `str` | Yes | Semantic version (e.g., "1.0.0"). |
| `nodes` | `List[Node]` | Yes | List of polymorphic node objects. |
| `edges` | `List[Edge]` | Yes | List of transition definitions. |
| `metadata` | `Dict[str, Any]` | No | Extension fields. |

### `Node` (Polymorphic)
Represents a step in the workflow.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `str` | Yes | Unique node ID within the workflow. |
| `type` | `NodeType` | Yes | Discriminator (TRIGGER, ACTION, CONDITION, END). |
| `properties` | `NodeProperties` | No | Type-specific configuration. |

### `Edge`
Represents a transition between nodes.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `str` | Yes | Unique edge ID. |
| `source` | `str` | Yes | ID of the source node. |
| `target` | `str` | Yes | ID of the target node. |
| `condition` | `str` | No | Expression to evaluate for traversal. |

## 2. Validation Rules

- **Uniqueness**: `WorkflowDefinition.id` must be unique across the entire registry.
- **Referential Integrity**: `Edge.source` and `Edge.target` must match existing `Node.id`s within the same workflow.
- **Connectivity**: Workflow must have at least one TRIGGER node and be graph-connected (checked by logic validator).
- **Naming**: IDs must match `^[a-z0-9_]+$` (snake_case).

## 3. Storage Schema (YAML)

File path: `src/definitions/workflows/{id}.yaml`

```yaml
id: approval_process_v1
name: "Document Approval"
version: "1.0.0"
nodes:
  - id: start
    type: TRIGGER
    properties:
      event: "doc_submitted"
  - id: manager_review
    type: ACTION
    properties:
      handler: "approval_service"
edges:
  - id: e1
    source: start
    target: manager_review
```
