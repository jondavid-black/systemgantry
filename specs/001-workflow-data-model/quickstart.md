# Quickstart: Adding a New Workflow

**Prerequisite**: Ensure you have checked out the repository and installed dependencies.

## 1. Create Definition File

Create a new file in `src/definitions/workflows/` (e.g., `my_new_flow.yaml`).

```bash
touch src/definitions/workflows/my_new_flow.yaml
```

## 2. Define Workflow Structure

Paste the following template into your file:

```yaml
id: my_new_flow
name: "My Example Workflow"
version: "0.1.0"
description: "A simple example workflow."

nodes:
  - id: start_node
    type: TRIGGER
    properties:
      event_type: "user_signup"
  
  - id: welcome_email
    type: ACTION
    properties:
      action_key: "send_email"
      payload:
        template: "welcome_v1"

edges:
  - id: flow_1
    source: start_node
    target: welcome_email
```

## 3. Validate Workflow

Run the validation script (TBD - implemented in this feature) to check your definition:

```bash
uv run python src/scripts/validate_workflows.py
```

## 4. Usage in Code

To load your workflow in code:

```python
from src.models.workflow.registry import WorkflowRegistry

registry = WorkflowRegistry()
registry.load_from_directory("src/definitions/workflows")

my_flow = registry.get_workflow("my_new_flow")
print(f"Loaded {my_flow.name} with {len(my_flow.nodes)} nodes")
```
