from typing import List, Set, Dict
from src.models.workflow.definition import WorkflowDefinition
from src.models.workflow.enums import WorkflowNodeType


def validate_workflow(workflow: WorkflowDefinition) -> List[str]:
    errors = []

    # Check for missing use_case_id (Warning/Optional check)
    if not workflow.use_case_id:
        # Not strictly an error based on spec, but good to warn if intended to be validated
        pass

    # Build adjacency list for graph traversal
    adj_list: Dict[str, List[str]] = {node.id: [] for node in workflow.nodes}
    node_ids = set(adj_list.keys())

    # Verify edges connect existing nodes
    for edge in workflow.edges:
        if edge.source_id not in node_ids:
            errors.append(f"Edge source {edge.source_id} does not exist")
            continue
        if edge.target_id not in node_ids:
            errors.append(f"Edge target {edge.target_id} does not exist")
            continue
        adj_list[edge.source_id].append(edge.target_id)

    # 1. Connectivity Check (Islands)
    # Start BFS from all Trigger nodes
    visited: Set[str] = set()
    queue: List[str] = []

    triggers = [n for n in workflow.nodes if n.type == WorkflowNodeType.TRIGGER]
    if not triggers:
        errors.append("Workflow must have at least one Trigger node")

    for trigger in triggers:
        if trigger.id not in visited:
            queue.append(trigger.id)
            visited.add(trigger.id)

    while queue:
        current = queue.pop(0)
        for neighbor in adj_list.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # Check for unreachable nodes
    unreachable = node_ids - visited
    if unreachable:
        errors.append(f"Unreachable nodes found (Islands): {', '.join(unreachable)}")

    # 2. Cycle Detection (DFS)
    recursion_stack: Set[str] = set()
    cycle_visited: Set[str] = set()

    def has_cycle(node_id: str) -> bool:
        cycle_visited.add(node_id)
        recursion_stack.add(node_id)

        for neighbor in adj_list.get(node_id, []):
            if neighbor not in cycle_visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in recursion_stack:
                return True

        recursion_stack.remove(node_id)
        return False

    for node_id in node_ids:
        if node_id not in cycle_visited:
            if has_cycle(node_id):
                errors.append(f"Cycle detected involving node {node_id}")
                break

    return errors
