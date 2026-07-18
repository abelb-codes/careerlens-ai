# ai/extractor/education.py
"""
Education extraction utilities for resume text.

This module identifies likely education entries from parsed resume text using
section detection and lightweight keyword heuristics.
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

EDUCATION_SECTION_HEADERS = {
    "academic background",
    "academics",
    "education",
    "educational background",
    "qualifications",
}
STOP_SECTION_HEADERS = {
    "certifications",
    "experience",
    "languages",
    "professional experience",
    "projects",
    "skills",
    "summary",
    "work experience",
}
DEGREE_KEYWORDS = (
    "bachelor",
    "bachelors",
    "b.sc",
    "bsc",
    "ba",
    "master",
    "masters",
    "m.sc",
    "msc",
    "ma",
    "mba",
    "phd",
    "ph.d",
    "doctorate",
    "diploma",
    "certificate",
    "associate",
    "degree",
)
INSTITUTION_KEYWORDS = (
    "college",
    "institute",
    "polytechnic",
    "school",
    "university",
)
YEAR_REGEX = re.compile(r"\b(?:19|20)\d{2}\b")


def extract_education(text: str) -> list[str]:
    """
    Extract likely education entries from resume text.

    Parameters
    ----------
    text:
        Plain resume text returned by the parser module.

    Returns
    -------
    list[str]
        Education entries as clean strings. Returns an empty list when no
        education information is found.
    """
    if not isinstance(text, str):
        logger.warning("Education extraction received non-string input.")
        return []

    lines = _non_empty_lines(text)
    education_lines = _section_lines(lines)

    if not education_lines:
        education_lines = [line for line in lines if _looks_like_education_line(line)]

    return _group_education_entries(education_lines)


def _non_empty_lines(text: str) -> list[str]:
    """Split text into stripped, non-empty lines."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def _section_lines(lines: list[str]) -> list[str]:
    """Return lines inside an education section when one exists."""
    collected_lines: list[str] = []
    inside_education_section = False

    for line in lines:
        normalized_line = _normalize_header(line)

        if normalized_line in EDUCATION_SECTION_HEADERS:
            inside_education_section = True
            continue

        if inside_education_section and normalized_line in STOP_SECTION_HEADERS:
            break

        if inside_education_section:
            collected_lines.append(line)

    return collected_lines


def _normalize_header(line: str) -> str:
    """Normalize a possible section header for comparison."""
    return line.strip(" :.-").lower()


def _looks_like_education_line(line: str) -> bool:
    """Return True when a line contains common education signals."""
    normalized_line = line.lower()
    return (
        any(keyword in normalized_line for keyword in DEGREE_KEYWORDS)
        or any(keyword in normalized_line for keyword in INSTITUTION_KEYWORDS)
        or bool(YEAR_REGEX.search(line))
    )


def _group_education_entries(lines: list[str]) -> list[str]:
    """Group nearby education lines into readable education entries."""
    entries: list[str] = []
    current_entry: list[str] = []

    for line in lines:
        if not _looks_like_education_line(line):
            continue

        starts_new_entry = bool(current_entry) and _starts_new_education_entry(line)
        if starts_new_entry:
            entries.append(" | ".join(current_entry))
            current_entry = []

        current_entry.append(line)

    if current_entry:
        entries.append(" | ".join(current_entry))

    return _deduplicate(entries)


def _starts_new_education_entry(line: str) -> bool:
    """Return True when a line is likely the beginning of another education item."""
    normalized_line = line.lower()
    return any(keyword in normalized_line for keyword in DEGREE_KEYWORDS)


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
