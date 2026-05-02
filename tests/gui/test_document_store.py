#!/usr/bin/env python3

"""
Tests for Markdown document persistence helpers.
"""

from pathlib import Path

from pygm.app.gui.document_store import (
    ACTIVE_MARKDOWN_FILE_KEY,
    get_active_markdown_file,
    read_markdown_file,
    set_active_markdown_file,
    write_markdown_file,
)


def test_active_markdown_file_is_empty_without_env(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Test that no active Markdown file is returned without configuration.
    :param tmp_path: Temporary path fixture.
    :param monkeypatch: Pytest monkeypatch fixture.
    :return: None.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv(ACTIVE_MARKDOWN_FILE_KEY, raising=False)

    assert get_active_markdown_file() is None


def test_active_markdown_file_is_persisted(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Test persisting and loading the active Markdown file path.
    :param tmp_path: Temporary path fixture.
    :param monkeypatch: Pytest monkeypatch fixture.
    :return: None.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv(ACTIVE_MARKDOWN_FILE_KEY, raising=False)
    markdown_file = tmp_path / "session.md"

    set_active_markdown_file(markdown_file)

    assert get_active_markdown_file() == markdown_file.resolve()


def test_markdown_file_read_write(
    tmp_path: Path,
) -> None:
    """
    Test reading and writing Markdown content.
    :param tmp_path: Temporary path fixture.
    :return: None.
    """
    markdown_file = tmp_path / "notes" / "session.md"
    content = "# Sitzung\n\nEin Dorf mit Geheimnissen."

    write_markdown_file(markdown_file, content)

    assert read_markdown_file(markdown_file) == content
