# ai/extractor/projects.py
"""
Project extraction utilities for resume text.

This module identifies likely project entries from parsed resume text using
section detection and lightweight project-specific heuristics.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

PROJECT_SECTION_HEADERS = {
    "academic projects",
    "key projects",
    "personal projects",
    "projects",
    "selected projects",
}
STOP_SECTION_HEADERS = {
    "certifications",
    "education",
    "experience",
    "languages",
    "professional experience",
    "skills",
    "summary",
    "work experience",
}
PROJECT_HINTS = (
    "application",
    "app",
    "built",
    "created",
    "dashboard",
    "developed",
    "github",
    "implemented",
    "platform",
    "project",
    "system",
    "tool",
    "website",
)
TECH_HINTS = (
    "angular",
    "django",
    "docker",
    "fastapi",
    "flask",
    "java",
    "javascript",
    "mongodb",
    "mysql",
    "node",
    "postgresql",
    "python",
    "react",
    "sql",
)


def extract_projects(text: str) -> list[str]:
    """
    Extract likely project entries from resume text.

    Parameters
    ----------
    text:
        Plain resume text returned by the parser module.

    Returns
    -------
    list[str]
        Project entries as clean strings. Returns an empty list when no
        project information is found.
    """
    if not isinstance(text, str):
        logger.warning("Project extraction received non-string input.")
        return []

    lines = _non_empty_lines(text)
    project_lines = _section_lines(lines)

    if not project_lines:
        project_lines = [line for line in lines if _looks_like_project_line(line)]

    return _group_project_entries(project_lines)


def _non_empty_lines(text: str) -> list[str]:
    """Split text into stripped, non-empty lines."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def _section_lines(lines: list[str]) -> list[str]:
    """Return lines inside a projects section when one exists."""
    collected_lines: list[str] = []
    inside_project_section = False

    for line in lines:
        normalized_line = _normalize_header(line)

        if normalized_line in PROJECT_SECTION_HEADERS:
            inside_project_section = True
            continue

        if inside_project_section and normalized_line in STOP_SECTION_HEADERS:
            break

        if inside_project_section:
            collected_lines.append(line)

    return collected_lines


def _normalize_header(line: str) -> str:
    """Normalize a possible section header for comparison."""
    return line.strip(" :.-").lower()


def _looks_like_project_line(line: str) -> bool:
    """Return True when a line contains common project signals."""
    normalized_line = line.lower()
    return (
        any(hint in normalized_line for hint in PROJECT_HINTS)
        or any(hint in normalized_line for hint in TECH_HINTS)
    )


def _group_project_entries(lines: list[str]) -> list[str]:
    """Group nearby project lines into readable project entries."""
    entries: list[str] = []
    current_entry: list[str] = []

    for line in lines:
        if not _looks_like_project_line(line):
            continue

        if current_entry and line.lower() in {item.lower() for item in current_entry}:
            continue

        if current_entry and _starts_new_project_entry(line):
            entries.append(" | ".join(current_entry))
            current_entry = []

        current_entry.append(line)

    if current_entry:
        entries.append(" | ".join(current_entry))

    return _deduplicate(entries)


def _starts_new_project_entry(line: str) -> bool:
    """Return True when a line likely starts a new project entry."""
    normalized_line = line.lower()
    has_project_hint = any(hint in normalized_line for hint in ("project", "system", "app", "platform"))
    return has_project_hint and len(line.split()) <= 8


def _deduplicate(items: list[str]) -> list[str]:
    """Remove duplicate entries while preserving order."""
    seen_items: set[str] = set()
    unique_items: list[str] = []

    for item in items:
        normalized_item = item.lower()
        if normalized_item not in seen_items:
            seen_items.add(normalized_item)
            unique_items.append(item)

    return unique_items
