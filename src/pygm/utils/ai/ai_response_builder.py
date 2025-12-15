#!/usr/bin/env python3

"""
AI response builder.

This module provides the AIResponseBuilder class for constructing
AIResponse instances using a fluent builder pattern with support
for content, finish reason, and error information.
"""

from pygm.utils.ai.ai_response import AIResponse


class AIResponseBuilder:
    """
    Builder for creating AIResponse instances.
    """

    def __init__(self, prompt_id: str, content: str = None) -> None:
        """
        Initialize the AIResponseBuilder.
        :param prompt_id: The prompt ID.
        :param content: The response content.
        """
        self._prompt_id: str = prompt_id
        self._content: str | None = content
        self._finish_reason: str | None = None
        self._error: str | None = None

    def set_content(self, content: str) -> "AIResponseBuilder":
        """
        Set the content of the response.
        :param content: the content
        :return: The builder instance.
        """
        self._content = content
        return self

    def set_finish_reason(self, finish_reason: str) -> "AIResponseBuilder":
        """
        Set the finish reason.
        :param finish_reason: The finish reason.
        :return: The builder instance.
        """
        self._finish_reason = finish_reason
        return self

    def set_error(self, error: str) -> "AIResponseBuilder":
        """
        Set the error message.
        :param error: The error message.
        :return: The builder instance.
        """
        self._error = error
        return self

    def build(self) -> AIResponse:
        """
        Build the AIResponse.
        :return: The constructed AIResponse.
        """
        return AIResponse(
            prompt_id=self._prompt_id,
            content=self._content,
            finish_reason=self._finish_reason,
            error=self._error,
        )
