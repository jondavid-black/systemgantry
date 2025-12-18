from typing import Optional
from pydantic import BaseModel


class ProcessProps(BaseModel):
    description: Optional[str] = None
    handler_ref: Optional[str] = None


class TriggerProps(BaseModel):
    event_type: str


class EmptyProps(BaseModel):
    pass
