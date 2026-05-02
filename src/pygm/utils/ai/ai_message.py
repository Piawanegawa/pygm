#!/usr/bin/env python3

"""
AI message model.

This module defines the AIMessage class representing a single message
in an AI conversation, consisting of a role and content.
"""

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
        Get the message role.
        :return: The message role.
        """
        return self.role

    def get_content(self) -> str:
        """
        Get the message content.
        :return: The message content.
        """
        return self.content
