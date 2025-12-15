from pygm.utils.ai.ai_message import AIMessage
from pygm.utils.ai.ai_message_role import AIMessageRole
from pygm.utils.ai.ai_prompt import AIPrompt


class AIPromptBuilder:
    """
    Builder for creating AIPrompt instances.
    """

    def __init__(self, prompt_id: str) -> None:
        """
        Initialize the AIPromptBuilder.

        :param prompt_id: The prompt ID.
        """
        self._prompt_id: str = prompt_id
        self._messages: list[AIMessage] = []
        self._max_output_tokens: int | None = None
        self._temperature: float | None = None

    def add_message(self, role: AIMessageRole, content: str) -> "AIPromptBuilder":
        """
        Add a message to the prompt.

        :param role: The role of the message sender.
        :param content: The content of the message.
        :return: The builder instance.
        """
        self._messages.append(AIMessage(role=role, content=content))
        return self

    def set_max_output_tokens(self, max_output_tokens: int) -> "AIPromptBuilder":
        """
        Set the max output tokens.

        :param max_output_tokens: The max output tokens.
        :return: The builder instance.
        """
        self._max_output_tokens = max_output_tokens
        return self

    def set_temperature(self, temperature: float) -> "AIPromptBuilder":
        """
        Set the temperature.

        :param temperature: The temperature.
        :return: The builder instance.
        """
        self._temperature = temperature
        return self

    def build(self) -> AIPrompt:
        """
        Build the AIPrompt.

        :return: The constructed AIPrompt.
        """
        return AIPrompt(
            prompt_id=self._prompt_id,
            messages=self._messages,
            max_output_tokens=self._max_output_tokens,
            temperature=self._temperature,
        )