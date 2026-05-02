#!/usr/bin/env python3

"""
AI provider factory.

This module provides the AIProviderFactory class for creating
AI provider instances based on the provider type specified
in the client configuration.
"""

from pygm.utils.ai.ai_client_config import AIClientConfig
from pygm.utils.ai.ai_provider import AIProvider
from pygm.utils.ai.ai_provider_type import AIProviderType
from pygm.utils.ai.impl.openrouter.openrouter_client_config import (
    OpenRouterClientConfig,
)
from pygm.utils.ai.impl.openrouter.openrouter_provider import OpenRouterProvider


class AIProviderFactory:
    """
    Factory for creating AI providers based on provider type.
    """

    @classmethod
    def create_ai_provider(cls, config: AIClientConfig) -> AIProvider:
        """
        Create an AI provider for the given client config.
        :param config: The client configuration containing the provider type.
        :return: The created AI provider.
        :raises ValueError: If the provider type is not supported.
        :raises TypeError: If config type does not match provider type.
        """
        provider_type = config.get_provider_type()
        if provider_type == AIProviderType.OPENROUTER:
            if isinstance(config, OpenRouterClientConfig):
                return OpenRouterProvider(config)
            raise TypeError("Expected OpenRouterClientConfig for OPENROUTER provider")
        raise ValueError(f"Unsupported provider type: {provider_type}")
