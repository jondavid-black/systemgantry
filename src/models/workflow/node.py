from typing import Generic, TypeVar, Literal, Union
from pydantic import BaseModel
from src.models.workflow.enums import WorkflowNodeType
from src.models.workflow.properties import ProcessProps, TriggerProps, EmptyProps

PropsT = TypeVar("PropsT", bound=BaseModel)


class BaseNode(BaseModel, Generic[PropsT]):
    id: str
    label: str
    type: WorkflowNodeType
    properties: PropsT


class ProcessNode(BaseNode[ProcessProps]):
    type: Literal[WorkflowNodeType.PROCESS]  # type: ignore
    properties: ProcessProps


class TriggerNode(BaseNode[TriggerProps]):
    type: Literal[WorkflowNodeType.TRIGGER]  # type: ignore
    properties: TriggerProps


class DecisionNode(BaseNode[EmptyProps]):
    type: Literal[WorkflowNodeType.DECISION]  # type: ignore
    properties: EmptyProps


class BranchNode(BaseNode[EmptyProps]):
    type: Literal[WorkflowNodeType.BRANCH]  # type: ignore
    properties: EmptyProps


class JoinNode(BaseNode[EmptyProps]):
    type: Literal[WorkflowNodeType.JOIN]  # type: ignore
    properties: EmptyProps


class CompletionNode(BaseNode[EmptyProps]):
    type: Literal[WorkflowNodeType.COMPLETION]  # type: ignore
    properties: EmptyProps


WorkflowNode = Union[
    ProcessNode, TriggerNode, DecisionNode, BranchNode, JoinNode, CompletionNode
]
