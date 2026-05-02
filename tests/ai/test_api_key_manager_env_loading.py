#!/usr/bin/env python3

"""
Tests for API key loading from multiple environment files.
"""

from pathlib import Path

from pygm.utils.ai.ai_provider_type import AIProviderType
from pygm.utils.ai.api_key_manager import ApiKeyManager


def test_api_key_manager_loads_key_from_later_env_file(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Test loading an API key when the first env file does not contain it.
    :param tmp_path: Temporary path fixture.
    :param monkeypatch: Pytest monkeypatch fixture.
    :return: None.
    """
    first_env_file = tmp_path / "first" / "pygm.env"
    second_env_file = tmp_path / "second" / "pygm.env"
    first_env_file.parent.mkdir()
    second_env_file.parent.mkdir()
    first_env_file.write_text("PYGM_ACTIVE_MARKDOWN_FILE='notes.md'\n", encoding="utf-8")
    second_env_file.write_text("OPENROUTER_API_KEY='test-key'\n", encoding="utf-8")
    monkeypatch.setattr(
        "pygm.utils.ai.api_key_manager.get_existing_env_file_candidates",
        lambda: [first_env_file, second_env_file],
    )
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    api_key_manager = ApiKeyManager()

    assert api_key_manager.get_api_key(AIProviderType.OPENROUTER).get_api_key() == "test-key"
