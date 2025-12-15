from abc import ABC, abstractmethod

from pygm.utils.ai.ai_prompt import AIPrompt
from pygm.utils.ai.ai_response import AIResponse


class AIClient(ABC):
    """
    Abstract interface for AI communication.
    """

    @abstractmethod
    def send_prompt(self, prompt: AIPrompt) -> AIResponse:
        """
        Send a prompt to the AI provider and receive a response.

        :param prompt: The AIPrompt to send.
        :return: The AIResponse from the provider.
        """
        pass