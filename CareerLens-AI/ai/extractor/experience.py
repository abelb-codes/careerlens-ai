# ai/extractor/experience.py
"""
Experience extraction utilities for resume text.

This module identifies likely work experience entries from parsed resume text
using section detection and lightweight employment heuristics.
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

EXPERIENCE_SECTION_HEADERS = {
    "employment history",
    "experience",
    "professional experience",
    "relevant experience",
    "work experience",
    "work history",
}
STOP_SECTION_HEADERS = {
    "certifications",
    "education",
    "languages",
    "projects",
    "references",
    "skills",
    "summary",
}
ROLE_KEYWORDS = (
    "administrator",
    "analyst",
    "architect",
    "assistant",
    "consultant",
    "coordinator",
    "designer",
    "developer",
    "director",
    "engineer",
    "executive",
    "intern",
    "lead",
    "manager",
    "officer",
    "specialist",
)
COMPANY_HINTS = (
    "company",
    "corp",
    "corporation",
    "inc",
    "limited",
    "llc",
    "ltd",
)
ACTION_VERBS = (
    "achieved",
    "built",
    "created",
    "designed",
    "developed",
    "implemented",
    "improved",
    "led",
    "managed",
    "optimized",
    "reduced",
    "supported",
)
DATE_RANGE_REGEX = re.compile(
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)?\.?\s*"
    r"(?:19|20)\d{2}\s*(?:-|to)\s*"
    r"(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)?\.?\s*)?"
    r"(?:(?:19|20)\d{2}|present|current|now)\b",
    re.IGNORECASE,
)
YEAR_REGEX = re.compile(r"\b(?:19|20)\d{2}\b")


def extract_experience(text: str) -> list[str]:
    """
    Extract likely work experience entries from resume text.

    Parameters
    ----------
    text:
        Plain resume text returned by the parser module.

    Returns
    -------
    list[str]
        Experience entries as clean strings. Returns an empty list when no
        experience information is found.
    """
    if not isinstance(text, str):
        logger.warning("Experience extraction received non-string input.")
        return []

    lines = _non_empty_lines(text)
    experience_lines = _section_lines(lines)

    if not experience_lines:
        experience_lines = [line for line in lines if _looks_like_experience_line(line)]

    return _group_experience_entries(experience_lines)


def _non_empty_lines(text: str) -> list[str]:
    """Split text into stripped, non-empty lines."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def _section_lines(lines: list[str]) -> list[str]:
    """Return lines inside an experience section when one exists."""
    collected_lines: list[str] = []
    inside_experience_section = False

    for line in lines:
        normalized_line = _normalize_header(line)

        if normalized_line in EXPERIENCE_SECTION_HEADERS:
            inside_experience_section = True
            continue

        if inside_experience_section and normalized_line in STOP_SECTION_HEADERS:
            break

        if inside_experience_section:
            collected_lines.append(line)

    return collected_lines


def _normalize_header(line: str) -> str:
    """Normalize a possible section header for comparison."""
    return line.strip(" :.-").lower()


def _looks_like_experience_line(line: str) -> bool:
    """Return True when a line contains common employment signals."""
    normalized_line = line.lower()
    return (
        any(keyword in normalized_line for keyword in ROLE_KEYWORDS)
        or any(hint in normalized_line for hint in COMPANY_HINTS)
        or any(verb in normalized_line for verb in ACTION_VERBS)
        or bool(DATE_RANGE_REGEX.search(line))
    )


def _group_experience_entries(lines: list[str]) -> list[str]:
    """Group nearby experience lines into readable experience entries."""
    entries: list[str] = []
    current_entry: list[str] = []

    for line in lines:
        if not _looks_like_experience_line(line):
            continue

        starts_new_entry = bool(current_entry) and _starts_new_experience_entry(line)
        if starts_new_entry:
            entries.append(" | ".join(current_entry))
            current_entry = []

        current_entry.append(line)

    if current_entry:
        entries.append(" | ".join(current_entry))

    return _deduplicate(entries)


def _starts_new_experience_entry(line: str) -> bool:
    """Return True when a line likely starts another work experience item."""
    normalized_line = line.lower()
    has_role = any(keyword in normalized_line for keyword in ROLE_KEYWORDS)
    has_company = any(hint in normalized_line for hint in COMPANY_HINTS)
    return has_role and has_company


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
