#!/usr/bin/env python3

"""
Tests for plothook GUI helper functions.
"""

from pygm.app.gui.plothook_tools import append_plothook_to_markdown, parse_plothooks


def test_parse_numbered_plothooks() -> None:
    """
    Test parsing numbered plothooks.
    :return: None.
    """
    response = "\n".join(
        [
            "1. A missing bell starts ringing under the old chapel.",
            "2. The innkeeper's shadow begins selling secrets at midnight.",
            "3. A river flows uphill toward a sealed dwarven gate.",
        ]
    )

    assert parse_plothooks(response) == [
        "A missing bell starts ringing under the old chapel.",
        "The innkeeper's shadow begins selling secrets at midnight.",
        "A river flows uphill toward a sealed dwarven gate.",
    ]


def test_parse_empty_response() -> None:
    """
    Test parsing an empty AI response.
    :return: None.
    """
    assert parse_plothooks("") == []


def test_parse_fallback_lines() -> None:
    """
    Test parsing non-numbered fallback lines.
    :return: None.
    """
    response = "\n".join(
        [
            "- A mirror refuses to reflect the town mayor.",
            "A storm leaves old coins instead of rain.",
        ]
    )

    assert parse_plothooks(response) == [
        "A mirror refuses to reflect the town mayor.",
        "A storm leaves old coins instead of rain.",
    ]


def test_append_plothook_to_empty_markdown() -> None:
    """
    Test appending a plothook to an empty Markdown document.
    :return: None.
    """
    assert append_plothook_to_markdown("", "A strange map sings.") == (
        "## Plothook\n\nA strange map sings.\n"
    )


def test_append_plothook_without_existing_heading() -> None:
    """
    Test appending a new Plothook section.
    :return: None.
    """
    markdown = "# Session Notes\n\nOpening scene."

    assert append_plothook_to_markdown(markdown, "The moon vanishes.") == (
        "# Session Notes\n\nOpening scene.\n\n## Plothook\n\nThe moon vanishes.\n"
    )


def test_append_plothook_with_existing_heading() -> None:
    """
    Test appending below an existing Plothook heading.
    :return: None.
    """
    markdown = "# Session Notes\n\n## Plothook\n\n- Existing hook.\n\n## NPCs\n\n- Mira"

    assert append_plothook_to_markdown(markdown, "A new hook appears.") == (
        "# Session Notes\n\n"
        "## Plothook\n\n"
        "- Existing hook.\n\n"
        "A new hook appears.\n\n"
        "## NPCs\n\n"
        "- Mira\n"
    )
