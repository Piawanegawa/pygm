#!/usr/bin/env python3

"""
API key manager.

This module provides the ApiKeyManager class for managing API keys
of different AI providers with persistence via dotenv environment files.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv, set_key

from pygm.utils.ai.ai_provider_type import AIProviderType
from pygm.utils.ai.api_key import ApiKey


class ApiKeyManager:
    """
    Manages API keys for different AI providers with persistence via dotenv.
    """

    ENV_FILE: str = "pygm.env"

    @classmethod
    def get_instance(cls) -> "ApiKeyManager":
        """
        Get the singleton instance of ApiKeyManager.
        :return: The ApiKeyManager instance.
        """
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the ApiKeyManager and load existing keys from env file.
        """
        self._api_keys: dict[AIProviderType, ApiKey] = {}
        self._load_from_env()

    def set_api_key(self, provider_type: AIProviderType, api_key: str) -> None:
        """
        Set an API key for a provider and persist it.
        :param provider_type: The type of AI provider.
        :param api_key: The ApiKey to store.
        """
        self._api_keys[provider_type] = ApiKey(provider_type, api_key)
        env_file_path = self._get_env_file_path()
        if not env_file_path.exists():
            env_file_path.touch()
        env_key = self._get_env_key_name(provider_type)
        set_key(str(env_file_path), env_key, api_key)

    def get_api_key(self, provider_type: AIProviderType) -> ApiKey:
        """
        Get the API key for a provider.
        :param provider_type: The type of AI provider.
        :return: The ApiKey object.
        :raises KeyError: If no API key is set for the provider.
        """
        if provider_type not in self._api_keys:
            raise KeyError(f"No API key set for provider: {provider_type.value}")
        return self._api_keys[provider_type]

    def _load_from_env(self) -> None:
        """
        Load API keys from the environment file.
        """
        env_file_path = self._get_env_file_path()
        if env_file_path.exists():
            load_dotenv(str(env_file_path))
        for provider_type in AIProviderType:
            env_key = self._get_env_key_name(provider_type)
            api_key_value = os.getenv(env_key)
            if api_key_value:
                self._api_keys[provider_type] = ApiKey(provider_type, api_key_value)

    @classmethod
    def _get_env_file_path(cls) -> Path:
        """
        Get the preferred environment file path.
        :return: The environment file path.
        """
        candidates = [Path.cwd() / cls.ENV_FILE]
        if getattr(sys, "frozen", False):
            candidates.append(Path(sys.executable).resolve().parent / cls.ENV_FILE)
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return candidates[0]

    @staticmethod
    def _get_env_key_name(provider_type: AIProviderType) -> str:
        """
        Get the environment variable name for a provider type.
        :param provider_type: The AI provider type.
        :return: The environment variable name.
        """
        return f"{provider_type.value}_API_KEY"
