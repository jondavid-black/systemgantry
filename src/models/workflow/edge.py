from typing import Optional
from pydantic import BaseModel, Field


class WorkflowEdge(BaseModel):
    source_id: str = Field(..., description="ID of the source node")
    target_id: str = Field(..., description="ID of the target node")
    condition: Optional[str] = Field(
        default=None, description="Logic expression for Decision outputs"
    )
