#!/usr/bin/env python3

"""
AI provider abstract base class.

This module defines the AIProvider abstract base class that serves as
the foundation for implementing AI provider integrations, including
methods for API endpoints, available models, and client creation.
"""

from abc import ABC, abstractmethod

from pygm.utils.ai.ai_client import AIClient
from pygm.utils.ai.ai_client_config import AIClientConfig
from pygm.utils.ai.ai_provider_type import AIProviderType


class AIProvider(ABC):
    """
    Abstract base class for AI providers.
    """

    def __init__(self, provider_type: AIProviderType) -> None:
        """
        Initialize the AIProvider.
        :param provider_type: The type of AI provider.
        """
        self._provider_type = provider_type

    def get_provider_type(self) -> AIProviderType:
        """
        Get the provider type.
        :return: The AI provider type.
        """
        return self._provider_type

    @abstractmethod
    def get_api_endpoint(self) -> str:
        """
        Get the API endpoint URL for this provider.
        :return: The API endpoint URL.
        """
        pass

    @abstractmethod
    def get_available_models(self) -> list[str]:
        """
        Get a list of available models for this provider.
        :return: List of available model names.
        """
        pass

    @abstractmethod
    def create_ai_client(self, config: AIClientConfig) -> AIClient:
        """
        Create an AI client with the given configuration.
        :param config: The client configuration.
        :return: An AIClient instance.
        """
        pass
