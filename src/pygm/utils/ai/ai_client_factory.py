#!/usr/bin/env python3

"""
AI client factory helpers.

This module provides small helper functions for creating configured AI clients.
"""

from pygm.utils.ai.ai_client import AIClient
from pygm.utils.ai.ai_client_config import AIClientConfig
from pygm.utils.ai.ai_client_config_builder import AIClientConfigBuilder
from pygm.utils.ai.ai_provider_factory import AIProviderFactory
from pygm.utils.ai.ai_provider_type import AIProviderType

DEFAULT_MODEL_ID: str = "openai/gpt-4o-mini"


def create_openrouter_ai_client(model_id: str = DEFAULT_MODEL_ID) -> AIClient:
    """
    Create an OpenRouter AI client.
    :param model_id: The OpenRouter model identifier.
    :return: The configured AI client.
    """
    config: AIClientConfig = (
        AIClientConfigBuilder(AIProviderType.OPENROUTER).set_model_id(model_id).build()
    )
    provider = AIProviderFactory.create_ai_provider(config)
    return provider.create_ai_client(config)
