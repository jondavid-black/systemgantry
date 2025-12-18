from enum import Enum


class WorkflowNodeType(str, Enum):
    TRIGGER = "TRIGGER"
    PROCESS = "PROCESS"
    DECISION = "DECISION"
    BRANCH = "BRANCH"
    JOIN = "JOIN"
    COMPLETION = "COMPLETION"
