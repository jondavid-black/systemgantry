import pytest
import uuid
from src.models.workflow.node import (
    TriggerNode,
    ProcessNode,
    CompletionNode,
)
from src.models.workflow.edge import WorkflowEdge
from src.models.workflow.definition import WorkflowDefinition
from src.models.workflow.properties import TriggerProps, ProcessProps, EmptyProps
from src.models.workflow.enums import WorkflowNodeType
from src.models.workflow.validation import validate_workflow


@pytest.fixture
def valid_workflow_data():
    trigger = TriggerNode(
        id="node-1",
        label="Start",
        type=WorkflowNodeType.TRIGGER,
        properties=TriggerProps(event_type="manual"),
    )
    process = ProcessNode(
        id="node-2",
        label="Process",
        type=WorkflowNodeType.PROCESS,
        properties=ProcessProps(description="Do something"),
    )
    completion = CompletionNode(
        id="node-3",
        label="End",
        type=WorkflowNodeType.COMPLETION,
        properties=EmptyProps(),
    )
    edges = [
        WorkflowEdge(source_id="node-1", target_id="node-2"),
        WorkflowEdge(source_id="node-2", target_id="node-3"),
    ]
    return {
        "id": uuid.uuid4(),
        "name": "Test Workflow",
        "use_case_id": "UC-TEST",
        "nodes": [trigger, process, completion],
        "edges": edges,
    }


def test_workflow_instantiation(valid_workflow_data):
    wf = WorkflowDefinition(**valid_workflow_data)
    assert wf.name == "Test Workflow"
    assert len(wf.nodes) == 3
    assert len(wf.edges) == 2


def test_validation_success(valid_workflow_data):
    wf = WorkflowDefinition(**valid_workflow_data)
    errors = validate_workflow(wf)
    assert len(errors) == 0


def test_validation_missing_trigger():
    # Only a process node, no trigger
    process = ProcessNode(
        id="node-1",
        label="Process",
        type=WorkflowNodeType.PROCESS,
        properties=ProcessProps(),
    )
    wf = WorkflowDefinition(
        id=uuid.uuid4(), name="Bad Workflow", nodes=[process], edges=[]
    )
    errors = validate_workflow(wf)
    assert any("must have at least one Trigger" in e for e in errors)


def test_validation_island_detection():
    # Trigger -> Process1. Process2 (disconnected).
    trigger = TriggerNode(
        id="node-1",
        label="Start",
        type=WorkflowNodeType.TRIGGER,
        properties=TriggerProps(event_type="m"),
    )
    p1 = ProcessNode(
        id="node-2",
        label="P1",
        type=WorkflowNodeType.PROCESS,
        properties=ProcessProps(),
    )
    p2 = ProcessNode(
        id="node-3",
        label="P2",
        type=WorkflowNodeType.PROCESS,
        properties=ProcessProps(),
    )

    edges = [WorkflowEdge(source_id="node-1", target_id="node-2")]

    wf = WorkflowDefinition(
        id=uuid.uuid4(), name="Island Workflow", nodes=[trigger, p1, p2], edges=edges
    )

    errors = validate_workflow(wf)
    assert any("Unreachable nodes found" in e for e in errors)
    assert "node-3" in str(errors)


def test_validation_cycle_detection():
    # Trigger -> A -> B -> A (cycle)
    trigger = TriggerNode(
        id="t",
        label="T",
        type=WorkflowNodeType.TRIGGER,
        properties=TriggerProps(event_type="m"),
    )
    a = ProcessNode(
        id="a", label="A", type=WorkflowNodeType.PROCESS, properties=ProcessProps()
    )
    b = ProcessNode(
        id="b", label="B", type=WorkflowNodeType.PROCESS, properties=ProcessProps()
    )

    edges = [
        WorkflowEdge(source_id="t", target_id="a"),
        WorkflowEdge(source_id="a", target_id="b"),
        WorkflowEdge(source_id="b", target_id="a"),  # Cycle back to A
    ]

    wf = WorkflowDefinition(
        id=uuid.uuid4(), name="Cycle Workflow", nodes=[trigger, a, b], edges=edges
    )

    errors = validate_workflow(wf)
    assert any("Cycle detected" in e for e in errors)


def test_validation_broken_edge_references():
    trigger = TriggerNode(
        id="t",
        label="T",
        type=WorkflowNodeType.TRIGGER,
        properties=TriggerProps(event_type="m"),
    )

    # Edge points to non-existent target "x"
    edges = [WorkflowEdge(source_id="t", target_id="x")]

    wf = WorkflowDefinition(
        id=uuid.uuid4(), name="Broken Edge", nodes=[trigger], edges=edges
    )

    errors = validate_workflow(wf)
    assert any("Edge target x does not exist" in e for e in errors)


def test_polymorphic_deserialization():
    # Test that JSON loading correctly types the nodes
    data = {
        "id": str(uuid.uuid4()),
        "name": "Poly Test",
        "nodes": [
            {
                "id": "t1",
                "label": "T",
                "type": "TRIGGER",
                "properties": {"event_type": "api"},
            },
            {
                "id": "p1",
                "label": "P",
                "type": "PROCESS",
                "properties": {"description": "desc", "handler_ref": "ref"},
            },
        ],
        "edges": [],
    }

    wf = WorkflowDefinition(**data)
    assert isinstance(wf.nodes[0], TriggerNode)
    assert isinstance(wf.nodes[1], ProcessNode)
    assert wf.nodes[0].properties.event_type == "api"
    assert wf.nodes[1].properties.handler_ref == "ref"
