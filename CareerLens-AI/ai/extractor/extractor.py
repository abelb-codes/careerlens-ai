"""
AI extraction orchestrator for resume information.

This module synthesizes extracted resume information from the parser output
and returns a normalized data structure matching the extractor contract.
"""

from __future__ import annotations

import logging
import re
from typing import TypedDict

from ai.extractor.education import extract_education
from ai.extractor.experience import extract_experience
from ai.extractor.personal_info import extract_personal_info
from ai.extractor.projects import extract_projects
from ai.extractor.skills import extract_skills

logger = logging.getLogger(__name__)

CERTIFICATIONS_SECTION_HEADERS = {
    "certifications",
    "certificates",
    "license",
    "licenses",
    "professional certifications",
    "certification",
}
LANGUAGES_SECTION_HEADERS = {
    "languages",
    "language",
    "spoken languages",
    "language proficiency",
    "languages spoken",
}
SECTION_BREAK_HEADERS = {
    "certifications",
    "education",
    "experience",
    "languages",
    "projects",
    "profile",
    "references",
    "skills",
    "summary",
    "work experience",
}
CERTIFICATION_KEYWORDS = (
    "certificat",
    "licensed",
    "license",
    "pmp",
    "cissp",
    "aws certified",
    "google cloud certified",
    "microsoft certified",
    "oracle certified",
    "scrum master",
)
NATURAL_LANGUAGES = (
    "english",
    "spanish",
    "french",
    "german",
    "mandarin",
    "chinese",
    "hindi",
    "arabic",
    "portuguese",
    "italian",
    "japanese",
    "korean",
    "swahili",
    "russian",
    "urdu",
    "bengali",
    "turkish",
    "vietnamese",
    "thai",
    "dutch",
)
LANGUAGE_PATTERN = re.compile(
    rf"(?<![A-Za-z])(?:{'|'.join(re.escape(lang) for lang in NATURAL_LANGUAGES)})(?![A-Za-z])",
    re.IGNORECASE,
)
CERTIFICATION_PATTERN = re.compile(
    rf"(?:{'|'.join(re.escape(keyword) for keyword in CERTIFICATION_KEYWORDS)})",
    re.IGNORECASE,
)


class ExtractionResult(TypedDict):
    name: str
    email: str
    phone: str
    skills: list[str]
    education: list[str]
    experience: list[str]
    projects: list[str]
    certifications: list[str]
    languages: list[str]


def extract_resume_data(text: str) -> ExtractionResult:
    """
    Extract normalized resume information from parsed text.

    Parameters
    ----------
    text:
        Plain resume text returned by the parser module.

    Returns
    -------
    ExtractionResult
        A dictionary matching the extractor contract.
    """
    if not isinstance(text, str):
        logger.warning("Resume extraction received non-string input.")
        return _empty_extraction_result()

    personal_info = extract_personal_info(text)
    return {
        "name": personal_info["name"],
        "email": personal_info["email"],
        "phone": personal_info["phone"],
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text),
        "certifications": _extract_certifications(text),
        "languages": _extract_languages(text),
    }


def _empty_extraction_result() -> ExtractionResult:
    """Return an empty extraction result preserving the contract."""
    return {
        "name": "",
        "email": "",
        "phone": "",
        "skills": [],
        "education": [],
        "experience": [],
        "projects": [],
        "certifications": [],
        "languages": [],
    }


def _non_empty_lines(text: str) -> list[str]:
    """Split text into stripped, non-empty lines."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def _normalize_header(line: str) -> str:
    """Normalize a possible section header for comparison."""
    return line.strip(" :.-").lower()


def _collect_section_lines(lines: list[str], headers: set[str]) -> list[str]:
    """Collect lines from a dedicated section until the next section header."""
    collected_lines: list[str] = []
    inside_section = False

    for line in lines:
        normalized_line = _normalize_header(line)

        if normalized_line in headers:
            inside_section = True
            continue

        if inside_section and normalized_line in SECTION_BREAK_HEADERS:
            break

        if inside_section:
            collected_lines.append(line)

    return collected_lines


def _extract_certifications(text: str) -> list[str]:
    """Extract certification entries from resume text."""
    lines = _non_empty_lines(text)
    section_lines = _collect_section_lines(lines, CERTIFICATIONS_SECTION_HEADERS)

    if section_lines:
        return _deduplicate([line for line in section_lines if line])

    fallback = [line for line in lines if CERTIFICATION_PATTERN.search(line)]
    return _deduplicate(fallback)


def _extract_languages(text: str) -> list[str]:
    """Extract natural language proficiencies from resume text."""
    lines = _non_empty_lines(text)
    section_lines = _collect_section_lines(lines, LANGUAGES_SECTION_HEADERS)

    if section_lines:
        tokens: list[str] = []
        for line in section_lines:
            for part in re.split(r"[,:;|]", line):
                token = part.strip()
                if token and LANGUAGE_PATTERN.search(token):
                    tokens.append(token)
        return _deduplicate(tokens)

    return _deduplicate(LANGUAGE_PATTERN.findall(text))


def _deduplicate(items: list[str]) -> list[str]:
    """Remove duplicate values while preserving original order."""
    seen: set[str] = set()
    unique: list[str] = []

    for item in items:
        normalized_item = item.strip().lower()
        if normalized_item and normalized_item not in seen:
            seen.add(normalized_item)
            unique.append(item.strip())

    return unique
