#!/usr/bin/env python3

"""
Plothook generator helpers.

This module provides pure helper functions for building prompts, parsing AI
responses, and inserting selected plothooks into Markdown text.
"""

import re

from pygm.utils.ai.ai_message_role import AIMessageRole
from pygm.utils.ai.ai_prompt import AIPrompt
from pygm.utils.ai.ai_prompt_builder import AIPromptBuilder

PLOTHOOK_HEADING: str = "## Plothook"
_NUMBERED_ITEM_PATTERN = re.compile(r"^\s*\d+[\.)]\s*(?P<content>.+?)\s*$")
_BULLET_ITEM_PATTERN = re.compile(r"^\s*[-*]\s*(?P<content>.+?)\s*$")
_PLOTHOOK_HEADING_PATTERN = re.compile(r"^##\s+Plothook\s*$")
_SECOND_LEVEL_HEADING_PATTERN = re.compile(r"^##\s+\S")


def build_plothook_prompt(restriction: str, count: int) -> AIPrompt:
    """
    Build a prompt for generating plothooks.
    :param restriction: The user-provided plothook restriction.
    :param count: The number of plothooks to generate.
    :return: The prompt to send to the AI provider.
    """
    clean_restriction = restriction.strip() or "any fantasy tabletop RPG adventure"
    instruction = (
        "Generate exactly "
        f"{count} short tabletop RPG plothook(s) based on this restriction: "
        f"{clean_restriction}. Each plothook must be one or two sentences. "
        "Return only a numbered list, one plothook per item."
    )
    return (
        AIPromptBuilder("plothook-generator")
        .add_message(AIMessageRole.SYSTEM, "You are a RPG Game Master Assistant.")
        .add_message(AIMessageRole.USER, instruction)
        .set_temperature(0.8)
        .set_max_output_tokens(500)
        .build()
    )


def parse_plothooks(response_content: str) -> list[str]:
    """
    Parse plothooks from an AI response.
    :param response_content: The raw AI response content.
    :return: Parsed plothooks.
    """
    lines = [line.strip() for line in response_content.splitlines() if line.strip()]
    numbered_items = _parse_numbered_items(lines)
    if numbered_items:
        return numbered_items
    return _parse_fallback_items(lines)


def append_plothook_to_markdown(markdown: str, plothook: str) -> str:
    """
    Append a selected plothook under the Plothook heading.
    :param markdown: The current Markdown document.
    :param plothook: The plothook to append.
    :return: The updated Markdown document.
    """
    clean_plothook = plothook.strip()
    if not markdown.strip():
        return f"{PLOTHOOK_HEADING}\n\n{clean_plothook}\n"

    lines = markdown.splitlines()
    heading_index = _find_plothook_heading(lines)
    if heading_index is None:
        return _append_new_plothook_section(markdown, clean_plothook)
    return _append_to_existing_plothook_section(lines, heading_index, clean_plothook)


def _parse_numbered_items(lines: list[str]) -> list[str]:
    """
    Parse numbered list items.
    :param lines: The response lines.
    :return: Parsed numbered items.
    """
    items: list[str] = []
    for line in lines:
        match = _NUMBERED_ITEM_PATTERN.match(line)
        if match:
            items.append(match.group("content"))
    return items


def _parse_fallback_items(lines: list[str]) -> list[str]:
    """
    Parse fallback list items from non-numbered responses.
    :param lines: The response lines.
    :return: Parsed fallback items.
    """
    items: list[str] = []
    for line in lines:
        bullet_match = _BULLET_ITEM_PATTERN.match(line)
        if bullet_match:
            items.append(bullet_match.group("content"))
        else:
            items.append(line)
    return items


def _find_plothook_heading(lines: list[str]) -> int | None:
    """
    Find the Plothook heading line index.
    :param lines: The Markdown lines.
    :return: The heading index or None.
    """
    for index, line in enumerate(lines):
        if _PLOTHOOK_HEADING_PATTERN.match(line):
            return index
    return None


def _append_new_plothook_section(markdown: str, plothook: str) -> str:
    """
    Append a new Plothook section.
    :param markdown: The current Markdown document.
    :param plothook: The plothook to append.
    :return: The updated Markdown document.
    """
    separator = "\n\n" if markdown.endswith("\n") else "\n\n"
    return f"{markdown.rstrip()}{separator}{PLOTHOOK_HEADING}\n\n{plothook}\n"


def _append_to_existing_plothook_section(
    lines: list[str],
    heading_index: int,
    plothook: str,
) -> str:
    """
    Append a plothook to an existing Plothook section.
    :param lines: The Markdown lines.
    :param heading_index: The Plothook heading index.
    :param plothook: The plothook to append.
    :return: The updated Markdown document.
    """
    insert_index = len(lines)
    for index in range(heading_index + 1, len(lines)):
        if _SECOND_LEVEL_HEADING_PATTERN.match(lines[index]):
            insert_index = index
            break

    new_lines = lines.copy()
    if insert_index == heading_index + 1:
        new_lines.insert(insert_index, "")
        insert_index += 1
    if insert_index > 0 and new_lines[insert_index - 1].strip():
        new_lines.insert(insert_index, "")
        insert_index += 1
    new_lines.insert(insert_index, plothook)
    if insert_index + 1 < len(new_lines) and _SECOND_LEVEL_HEADING_PATTERN.match(
        new_lines[insert_index + 1]
    ):
        new_lines.insert(insert_index + 1, "")
    return "\n".join(new_lines).rstrip() + "\n"
