#!/usr/bin/env python3

"""
AI provider type enumeration.

This module defines the AIProviderType enum representing the different
supported AI provider integrations (e.g., OpenRouter).
"""

from enum import Enum


class AIProviderType(Enum):
    """
    Supported AI provider types.
    """

    OPENROUTER = "OPENROUTER"
    TEST = "TEST"
