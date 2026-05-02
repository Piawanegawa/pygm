#!/usr/bin/env python3

"""
Tests for AI providers.
"""

from pygm.utils.ai.ai_provider_type import AIProviderType
from pygm.utils.ai.api_key import ApiKey
from pygm.utils.ai.impl.openrouter.openrouter_client_config import OpenRouterClientConfig
from pygm.utils.ai.impl.openrouter.openrouter_provider import OpenRouterProvider


def test_openrouter_provider_sets_authorization_header(monkeypatch) -> None:
    """
    Test that OpenRouter client creation sets an explicit authorization header.
    :param monkeypatch: Pytest monkeypatch fixture.
    :return: None.
    """
    captured_kwargs = {}

    class FakeOpenAI:
        """
        Fake OpenAI client for capturing constructor arguments.
        """

        def __init__(self, **kwargs) -> None:
            """
            Capture constructor arguments.
            :param kwargs: Constructor keyword arguments.
            """
            captured_kwargs.update(kwargs)

    monkeypatch.setattr(
        "pygm.utils.ai.impl.openrouter.openrouter_provider.OpenAI",
        FakeOpenAI,
    )

    OpenRouterProvider(
        OpenRouterClientConfig(
            api_key=ApiKey(AIProviderType.OPENROUTER, "test-key"),
            model_id="test-model",
        )
    )

    assert captured_kwargs["api_key"] == "test-key"
    assert captured_kwargs["default_headers"]["Authorization"] == "Bearer test-key"
