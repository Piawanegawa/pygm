from pydantic import BaseModel

from pygm.utils.ai.ai_message_role import AIMessageRole


class AIMessage(BaseModel):
    """
    Represents a message in an AI conversation.
    """

    role: AIMessageRole
    content: str

    def get_role(self) -> AIMessageRole:
        """
        Get the role of the message.

        :return: The message role.
        """
        return self.role

    def get_content(self) -> str:
        """
        Get the content of the message.

        :return: The message content.
        """
        return self.content