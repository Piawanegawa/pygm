from enum import Enum


class AIMessageRole(Enum):
    """
    Roles for messages in AI conversations.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"