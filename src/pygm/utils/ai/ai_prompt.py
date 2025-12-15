from pydantic import BaseModel

from pygm.utils.ai.ai_message import AIMessage


class AIPrompt(BaseModel):
    """
    Represents a prompt to send to an AI provider.
    """

    prompt_id: str
    messages: list[AIMessage]
    max_output_tokens: int | None = None
    temperature: float | None = None

    def get_prompt_id(self) -> str:
        """
        Get the prompt ID.
        :return: The prompt ID.
        """
        return self.prompt_id

    def get_messages(self) -> list[AIMessage]:
        """
        Get the messages.
        :return: The list of messages.
        """
        return self.messages

    def get_max_output_tokens(self) -> int | None:
        """
        Get the max output tokens.
        :return: The max output tokens or None.
        """
        return self.max_output_tokens

    def get_temperature(self) -> float | None:
        """
        Get the temperature.
        :return: The temperature or None.
        """
        return self.temperature