#!/usr/bin/env python3

"""
AI message role enumeration.

This module defines the AIMessageRole enum representing the different
roles a message can have in an AI conversation (system, user, assistant, tool).
"""

from enum import Enum


class AIMessageRole(Enum):
    """
    Roles for messages in AI conversations.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
