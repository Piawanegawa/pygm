#!/usr/bin/env python3

"""
AI client configuration.

This module defines the AIClientConfig base class for configuring AI clients
with provider-specific settings like API keys and model identifiers.
"""

from pygm.utils.ai.ai_provider_type import AIProviderType
from pygm.utils.ai.api_key import ApiKey


class AIClientConfig:
    """
    Abstract base class for AI client configurations.
    """

    def __init__(self, api_key: ApiKey, model_id: str | None) -> None:
        """
        Initialize the AIClientConfig.
        :param api_key: The API key for authentication.
        :param model_id: The model identifier to be used.
        """
        self._api_key: ApiKey = api_key
        self._model_id: str | None = model_id

    def get_provider_type(self) -> AIProviderType:
        """
        Get the provider type for this configuration.
        :return: The AI provider type.
        """
        return self._api_key.get_provider_type()

    def get_api_key(self) -> str:
        """
        Get the API key string.
        :return: The API key string.
        """
        return self._api_key.get_api_key()

    def get_model_id(self) -> str | None:
        """
        Get the model identifier.
        :return: The model identifier, or None if not set.
        """
        return self._model_id
