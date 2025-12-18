# Quickstart - Workflow Definitions

## Overview
This feature provides the Data Elements to model business workflows. It uses Pydantic for validation and SQLAlchemy for persistence.

## Installation
The models are part of the core source. No extra installation required.

## Usage Guide

### 1. Creating a Workflow (Python)

```python
from src.models.workflow.node import TriggerNode, ProcessNode, WorkflowEdge
from src.models.workflow.definition import WorkflowDefinition
from src.models.workflow.properties import TriggerProps, ProcessProps
from src.models.workflow.enums import WorkflowNodeType
from uuid import uuid4

# 1. Define Nodes
trigger = TriggerNode(
    id="start", 
    label="Start Event", 
    type=WorkflowNodeType.TRIGGER,
    properties=TriggerProps(event_type="manual")
)

step1 = ProcessNode(
    id="step-1", 
    label="Approver Step", 
    type=WorkflowNodeType.PROCESS,
    properties=ProcessProps(handler_ref="services.approvals.request")
)

# 2. Define Edges
edge = WorkflowEdge(source_id="start", target_id="step-1")

# 3. Create Workflow
wf = WorkflowDefinition(
    id=uuid4(),
    name="Approval Flow",
    use_case_id="UC-001",
    nodes=[trigger, step1],
    edges=[edge]
)

# 4. Validate (Graph Check)
from src.models.workflow.validation import validate_workflow
errors = validate_workflow(wf)
if errors:
    print("Invalid structure:", errors)
```

### 2. Validation Rules
The `validate_workflow` function checks:
- **Connectivity**: All nodes must be reachable from a Trigger.
- **Cycles**: No infinite loops (unless explicitly allowed, currently warnings).
- **Integrity**: Edges must point to existing Node IDs.

### 3. Example Output
Running `src/scripts/seed_workflow.py` produces:

```json
{
  "id": "49ef6608-9eb4-470c-93bb-9caa7517ec39",
  "name": "Sample Approval Workflow",
  "description": "A test workflow with all node types",
  "use_case_id": "UC-101",
  "nodes": [
    {
      "id": "node-1",
      "label": "Start Request",
      "type": "TRIGGER",
      "properties": {
        "event_type": "http_request"
      }
    },
    ...
  ],
  "edges": [ ... ]
}
```
