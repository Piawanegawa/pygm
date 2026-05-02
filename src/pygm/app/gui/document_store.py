#!/usr/bin/env python3

"""
Markdown document persistence helpers.

This module provides file and setting helpers for the active Markdown document.
"""

import os
from pathlib import Path

from dotenv import load_dotenv, set_key

from pygm.app.config_paths import (
    get_existing_env_file_candidates,
    get_preferred_env_file_path,
)

ACTIVE_MARKDOWN_FILE_KEY: str = "PYGM_ACTIVE_MARKDOWN_FILE"
MARKDOWN_FILE_FILTER: str = "Markdown files (*.md *.markdown);;All files (*)"


def get_active_markdown_file() -> Path | None:
    """
    Get the persisted active Markdown file.
    :return: The active Markdown file path or None.
    """
    for env_file_path in get_existing_env_file_candidates():
        load_dotenv(str(env_file_path), override=True)
    active_file = os.getenv(ACTIVE_MARKDOWN_FILE_KEY)
    if not active_file:
        return None
    return Path(active_file)


def set_active_markdown_file(file_path: Path) -> None:
    """
    Persist the active Markdown file path.
    :param file_path: The Markdown file path.
    :return: None.
    """
    env_file_path = get_preferred_env_file_path()
    if not env_file_path.exists():
        env_file_path.touch()
    set_key(str(env_file_path), ACTIVE_MARKDOWN_FILE_KEY, str(file_path.resolve()))


def read_markdown_file(file_path: Path) -> str:
    """
    Read Markdown text from a file.
    :param file_path: The Markdown file path.
    :return: The file content.
    """
    return file_path.read_text(encoding="utf-8")


def write_markdown_file(file_path: Path, content: str) -> None:
    """
    Write Markdown text to a file.
    :param file_path: The Markdown file path.
    :param content: The Markdown content.
    :return: None.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")

