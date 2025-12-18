from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from src.models.workflow.node import WorkflowNode
from src.models.workflow.edge import WorkflowEdge


class WorkflowDefinition(BaseModel):
    id: UUID = Field(..., description="Unique Identifier")
    name: str = Field(..., description="Human-readable name")
    description: Optional[str] = None
    use_case_id: Optional[str] = Field(
        default=None, description="Traceability link to Use Case"
    )
    nodes: List[WorkflowNode] = Field(..., description="List of workflow nodes")
    edges: List[WorkflowEdge] = Field(..., description="List of workflow connections")
