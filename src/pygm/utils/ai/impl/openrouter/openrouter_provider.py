#!/usr/bin/env python3

"""
OpenRouter provider implementation.

This module provides the OpenRouterProvider class, which implements the AIProvider
interface for creating and managing OpenRouter API clients.
"""

from openai import OpenAI

from pygm.utils.ai.ai_client import AIClient
from pygm.utils.ai.ai_client_config import AIClientConfig
from pygm.utils.ai.ai_provider import AIProvider
from pygm.utils.ai.ai_provider_type import AIProviderType
from pygm.utils.ai.impl.openrouter.openrouter_client import OpenRouterClient
from pygm.utils.ai.impl.openrouter.openrouter_client_config import (
    OpenRouterClientConfig,
)


class OpenRouterProvider(AIProvider):
    """
    AI Provider for OpenRouter using the OpenAI-compatible API.
    """

    _API_ENDPOINT: str = "https://openrouter.ai/api/v1"

    def __init__(self, config: OpenRouterClientConfig) -> None:
        """
        Initialize the OpenRouter provider.
        :param config: Configuration for the OpenRouter client.
        """
        super().__init__(AIProviderType.OPENROUTER)
        self._config: OpenRouterClientConfig = config
        self._client: OpenAI = self._create_client()

    def get_api_endpoint(self) -> str:
        """
        Return the API endpoint for OpenRouter.
        :return: The API endpoint URL.
        """
        return self._API_ENDPOINT

    def get_available_models(self) -> list[str]:
        """
        Return a list of available models from OpenRouter API.
        :return: List of model identifiers.
        """
        models = self._client.models.list()
        return [model.id for model in models.data]

    def create_ai_client(self, config: AIClientConfig) -> AIClient:
        """
        Create an AI client based on the provided configuration.
        :param config: Configuration for the AI client.
        :return: the AI client instance.
        """
        if isinstance(config, OpenRouterClientConfig):
            return OpenRouterClient(
                client=self._client,
                model=config.get_model_id(),
            )
        raise ValueError("Invalid config type for OpenRouterProvider")

    def _create_client(self) -> OpenAI:
        """
        Create the OpenAI client configured for OpenRouter.
        :return: Configured OpenAI client.
        """
        return OpenAI(
            base_url=self._API_ENDPOINT,
            api_key=self._config.get_api_key(),
        )
