import uuid
from src.models.workflow.node import (
    TriggerNode,
    ProcessNode,
    DecisionNode,
    BranchNode,
    JoinNode,
    CompletionNode,
)
from src.models.workflow.edge import WorkflowEdge
from src.models.workflow.definition import WorkflowDefinition
from src.models.workflow.properties import TriggerProps, ProcessProps, EmptyProps
from src.models.workflow.enums import WorkflowNodeType
from src.models.workflow.validation import validate_workflow


def run_seed():
    print("Creating workflow nodes...")

    # 1. Trigger
    trigger = TriggerNode(
        id="node-1",
        label="Start Request",
        type=WorkflowNodeType.TRIGGER,
        properties=TriggerProps(event_type="http_request"),
    )

    # 2. Process
    process = ProcessNode(
        id="node-2",
        label="Validate Data",
        type=WorkflowNodeType.PROCESS,
        properties=ProcessProps(
            description="Validates incoming payload",
            handler_ref="services.validation.validate",
        ),
    )

    # 3. Decision
    decision = DecisionNode(
        id="node-3",
        label="Is Valid?",
        type=WorkflowNodeType.DECISION,
        properties=EmptyProps(),
    )

    # 4. Branch (Parallel)
    branch = BranchNode(
        id="node-4",
        label="Split Processing",
        type=WorkflowNodeType.BRANCH,
        properties=EmptyProps(),
    )

    # 5. Parallel Process A
    proc_a = ProcessNode(
        id="node-5",
        label="Process A",
        type=WorkflowNodeType.PROCESS,
        properties=ProcessProps(description="Do A"),
    )

    # 6. Parallel Process B
    proc_b = ProcessNode(
        id="node-6",
        label="Process B",
        type=WorkflowNodeType.PROCESS,
        properties=ProcessProps(description="Do B"),
    )

    # 7. Join
    join = JoinNode(
        id="node-7",
        label="Merge Results",
        type=WorkflowNodeType.JOIN,
        properties=EmptyProps(),
    )

    # 8. Completion
    completion = CompletionNode(
        id="node-8",
        label="End",
        type=WorkflowNodeType.COMPLETION,
        properties=EmptyProps(),
    )

    print("Creating edges...")
    edges = [
        WorkflowEdge(source_id="node-1", target_id="node-2"),
        WorkflowEdge(source_id="node-2", target_id="node-3"),
        WorkflowEdge(source_id="node-3", target_id="node-4", condition="true"),
        WorkflowEdge(source_id="node-4", target_id="node-5"),
        WorkflowEdge(source_id="node-4", target_id="node-6"),
        WorkflowEdge(source_id="node-5", target_id="node-7"),
        WorkflowEdge(source_id="node-6", target_id="node-7"),
        WorkflowEdge(source_id="node-7", target_id="node-8"),
    ]

    print("Assembling Workflow Definition...")
    wf = WorkflowDefinition(
        id=uuid.uuid4(),
        name="Sample Approval Workflow",
        description="A test workflow with all node types",
        use_case_id="UC-101",
        nodes=[trigger, process, decision, branch, proc_a, proc_b, join, completion],
        edges=edges,
    )

    print(f"\nWorkflow Created: {wf.name} ({wf.id})")
    print(f"Nodes: {len(wf.nodes)}")
    print(f"Edges: {len(wf.edges)}")

    print("\nValidating Workflow...")
    errors = validate_workflow(wf)

    if errors:
        print("❌ Validation Failed:")
        for e in errors:
            print(f" - {e}")
    else:
        print("✅ Validation Passed!")

    # Test JSON Serialization
    print("\nJSON Serialization Test:")
    print(wf.model_dump_json(indent=2))


if __name__ == "__main__":
    run_seed()
