#!/usr/bin/env python3

"""
AI client interface.

This module defines the abstract AIClient interface for communicating
with AI providers. Concrete implementations handle provider-specific API calls.
"""

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
