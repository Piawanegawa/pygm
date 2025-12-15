from pydantic import BaseModel

from pygm.utils.ai.ai_message_role import AIMessageRole


class AIMessage(BaseModel):
    """
    Represents a message in an AI conversation.
    """

    role: AIMessageRole
    content: str
