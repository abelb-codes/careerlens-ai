"""
ATS compatibility scoring utilities for CareerLens AI.

This module computes an ATS-friendly score from normalized resume information.
It evaluates whether extracted resume sections are present in a way that makes a
resume easier for applicant tracking systems to parse.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

MAX_SKILLS_COUNT = 3
MAX_EDUCATION_ENTRIES = 1
MAX_EXPERIENCE_ENTRIES = 1
MAX_PROJECT_ENTRIES = 1
MAX_EXTRAS_ENTRIES = 1

CONTACT_FIELD_WEIGHT = 5
SKILLS_WEIGHT = 20
EDUCATION_WEIGHT = 20
EXPERIENCE_WEIGHT = 25
PROJECT_WEIGHT = 10
EXTRAS_WEIGHT = 10


def calculate_ats_score(extracted_resume: dict[str, Any]) -> int:
    """
    Calculate an ATS compatibility score from normalized resume data.

    Parameters
    ----------
    extracted_resume:
        A dictionary produced by the extractor contract.

    Returns
    -------
    int
        An integer score from 0 to 100 representing ATS friendliness.
    """
    if not isinstance(extracted_resume, dict):
        logger.warning("ATS score calculation received non-dict input.")
        return 0

    name = _extract_string(extracted_resume.get("name"))
    email = _extract_string(extracted_resume.get("email"))
    phone = _extract_string(extracted_resume.get("phone"))
    skills = _extract_list(extracted_resume.get("skills"))
    education = _extract_list(extracted_resume.get("education"))
    experience = _extract_list(extracted_resume.get("experience"))
    projects = _extract_list(extracted_resume.get("projects"))
    certifications = _extract_list(extracted_resume.get("certifications"))
    languages = _extract_list(extracted_resume.get("languages"))

    contact_score = (
        bool(name) * CONTACT_FIELD_WEIGHT
        + bool(email) * CONTACT_FIELD_WEIGHT
        + bool(phone) * CONTACT_FIELD_WEIGHT
    )
    skills_score = _calculate_section_score(len(skills), MAX_SKILLS_COUNT, SKILLS_WEIGHT)
    education_score = _calculate_section_score(
        len(education), MAX_EDUCATION_ENTRIES, EDUCATION_WEIGHT
    )
    experience_score = _calculate_section_score(
        len(experience), MAX_EXPERIENCE_ENTRIES, EXPERIENCE_WEIGHT
    )
    project_score = _calculate_section_score(
        len(projects), MAX_PROJECT_ENTRIES, PROJECT_WEIGHT
    )
    extras_score = _calculate_section_score(
        len(certifications) + len(languages), MAX_EXTRAS_ENTRIES, EXTRAS_WEIGHT
    )

    total_score = (
        contact_score
        + skills_score
        + education_score
        + experience_score
        + project_score
        + extras_score
    )

    normalized_score = max(0, min(100, round(total_score)))
    logger.debug(
        "ATS score breakdown: contact=%s skills=%s education=%s experience=%s projects=%s extras=%s total=%s",
        contact_score,
        skills_score,
        education_score,
        experience_score,
        project_score,
        extras_score,
        normalized_score,
    )
    return normalized_score


def _calculate_section_score(count: int, max_count: int, weight: int) -> float:
    """Compute a normalized score for a list-style section."""
    if count <= 0:
        return 0.0

    normalized_count = min(count, max_count) / max_count
    return normalized_count * weight


def _extract_string(value: Any) -> str:
    """Convert a value to a stripped string if possible."""
    if isinstance(value, str):
        return value.strip()
    return ""


def _extract_list(value: Any) -> list[str]:
    """Convert a value to a list of stripped strings if possible."""
    if isinstance(value, list):
        return [str(item).strip() for item in value if isinstance(item, str) and item.strip()]
    return []
