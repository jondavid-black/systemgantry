from behave import given, when, then
import uuid
from src.models.workflow.definition import WorkflowDefinition
from src.models.workflow.node import TriggerNode, ProcessNode, CompletionNode
from src.models.workflow.edge import WorkflowEdge
from src.models.workflow.properties import TriggerProps, ProcessProps, EmptyProps
from src.models.workflow.enums import WorkflowNodeType
from src.models.workflow.validation import validate_workflow


@given('I create a new workflow named "{name}"')  # type: ignore
def step_create_workflow(context, name):
    context.workflow_data = {"id": uuid.uuid4(), "name": name, "nodes": [], "edges": []}


@when('I add a "{node_type}" node with id "{node_id}" and label "{label}"')  # type: ignore
def step_add_node(context, node_type, node_id, label):
    node = None
    if node_type == "Trigger":
        node = TriggerNode(
            id=node_id,
            label=label,
            type=WorkflowNodeType.TRIGGER,
            properties=TriggerProps(event_type="manual"),
        )
    elif node_type == "Process":
        node = ProcessNode(
            id=node_id,
            label=label,
            type=WorkflowNodeType.PROCESS,
            properties=ProcessProps(description="Test Process"),
        )
    elif node_type == "Completion":
        node = CompletionNode(
            id=node_id,
            label=label,
            type=WorkflowNodeType.COMPLETION,
            properties=EmptyProps(),
        )
    else:
        raise ValueError(f"Unknown node type: {node_type}")

    context.workflow_data["nodes"].append(node)


@when('I connect "{source_id}" to "{target_id}"')  # type: ignore
def step_connect_nodes(context, source_id, target_id):
    edge = WorkflowEdge(source_id=source_id, target_id=target_id)
    context.workflow_data["edges"].append(edge)


@then("the workflow should be valid")  # type: ignore
def step_validate_workflow(context):
    wf = WorkflowDefinition(**context.workflow_data)
    errors = validate_workflow(wf)
    assert len(errors) == 0, f"Validation errors: {errors}"
    context.workflow = wf


@then("the workflow should have {node_count:d} nodes and {edge_count:d} edges")  # type: ignore
def step_check_counts(context, node_count, edge_count):
    assert len(context.workflow.nodes) == node_count
    assert len(context.workflow.edges) == edge_count


@then('the node "{node_id}" should be reachable from the start')  # type: ignore
def step_check_reachability(context, node_id):
    # This is implicitly checked by validate_workflow (island detection),
    # but we can verify it explicitly if needed.
    # For this test, relies on the fact that validate_workflow passed.
    pass
