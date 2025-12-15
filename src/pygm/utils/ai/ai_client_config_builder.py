#!/usr/bin/env python3

"""
AI client configuration builder.

This module provides the AIClientConfigBuilder class for constructing
AIClientConfig instances with a fluent builder pattern.
"""

from pygm.utils.ai.ai_client_config import AIClientConfig
from pygm.utils.ai.ai_provider_type import AIProviderType
from pygm.utils.ai.api_key import ApiKey
from pygm.utils.ai.api_key_manager import ApiKeyManager


class AIClientConfigBuilder:
    """
    Builder for creating AIClientConfig instances.
    """

    def __init__(self, provider_type: AIProviderType) -> None:
        """
        Initialize the AIClientConfigBuilder.
        :param provider_type: The AI provider type.
        """
        self._provider_type: AIProviderType = provider_type
        self._api_key: str | None = None
        self._model_id: str | None = None

    def set_api_key(self, api_key: str) -> "AIClientConfigBuilder":
        """
        Set the API key.
        :param api_key: The API key.
        :return: The builder instance.
        """
        self._api_key = api_key
        return self

    def build(self) -> AIClientConfig:
        """
        Build the AIClientConfig.
        :return: The constructed AIClientConfig.
        :raises ValueError: If required fields are missing or provider type unsupported.
        """
        api_key = self._resolve_api_key()
        if self._provider_type == AIProviderType.OPENROUTER:
            from pygm.utils.ai.impl.openrouter.openrouter_client_config import (
                OpenRouterClientConfig,
            )

            return OpenRouterClientConfig(api_key=api_key, model_id=self._model_id)
        raise ValueError(f"Unsupported provider type: {self._provider_type}")

    def _resolve_api_key(self) -> ApiKey:
        """
        Resolve the API key from explicit value or ApiKeyManager fallback.
        :return: The resolved ApiKey.
        :raises ValueError: If no API key is available.
        """
        if self._api_key is not None:
            return ApiKey(provider_type=self._provider_type, api_key=self._api_key)
        stored_key = ApiKeyManager().get_api_key(self._provider_type)
        if stored_key is not None:
            return stored_key
        raise ValueError("API key is required")
