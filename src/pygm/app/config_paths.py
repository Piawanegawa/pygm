#!/usr/bin/env python3

"""
Application configuration path helpers.

This module provides shared helpers for locating pygm environment files.
"""

import sys
from pathlib import Path

ENV_FILE: str = "pygm.env"


def get_env_file_candidates() -> list[Path]:
    """
    Get candidate environment file paths.
    :return: Candidate environment file paths.
    """
    candidates = [Path.cwd() / ENV_FILE]
    if getattr(sys, "frozen", False):
        candidates.append(Path(sys.executable).resolve().parent / ENV_FILE)
    return _deduplicate_paths(candidates)


def get_existing_env_file_candidates() -> list[Path]:
    """
    Get existing candidate environment file paths.
    :return: Existing candidate environment file paths.
    """
    return [candidate for candidate in get_env_file_candidates() if candidate.exists()]


def get_preferred_env_file_path() -> Path:
    """
    Get the preferred environment file path for writes.
    :return: The preferred environment file path.
    """
    candidates = get_env_file_candidates()
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _deduplicate_paths(paths: list[Path]) -> list[Path]:
    """
    Deduplicate paths while preserving order.
    :param paths: The paths to deduplicate.
    :return: Deduplicated paths.
    """
    deduplicated_paths: list[Path] = []
    seen_paths: set[Path] = set()
    for path in paths:
        resolved_path = path.resolve()
        if resolved_path not in seen_paths:
            deduplicated_paths.append(path)
            seen_paths.add(resolved_path)
    return deduplicated_paths
