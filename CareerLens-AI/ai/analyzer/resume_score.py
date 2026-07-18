"""
Resume quality scoring for CareerLens AI.

This module computes a heuristic resume score from normalized extractor output.
It focuses on completeness, structure, and content density using resume fields
already extracted by the information extraction layer.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

CONTACT_SCORE_WEIGHT = 10
SKILLS_SCORE_WEIGHT = 20
EDUCATION_SCORE_WEIGHT = 20
EXPERIENCE_SCORE_WEIGHT = 25
PROJECTS_SCORE_WEIGHT = 10
EXTRAS_SCORE_WEIGHT = 15

MAX_SKILLS_COUNT = 10
MAX_EDUCATION_ENTRIES = 3
MAX_EXPERIENCE_ENTRIES = 3
MAX_PROJECTS_ENTRIES = 2
MAX_EXTRAS_ENTRIES = 2


def calculate_resume_score(extracted_resume: dict[str, Any]) -> int:
    """
    Calculate a resume quality score from normalized extracted resume data.

    Parameters
    ----------
    extracted_resume:
        A dictionary following the extractor contract.

    Returns
    -------
    int
        A score from 0 to 100 representing resume quality.
    """
    if not isinstance(extracted_resume, dict):
        logger.warning("Resume score calculation received non-dict input.")
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

    contact_score = _calculate_contact_score(name=name, email=email, phone=phone)
    skills_score = _calculate_list_score(
        count=len(skills),
        max_count=MAX_SKILLS_COUNT,
        weight=SKILLS_SCORE_WEIGHT,
    )
    education_score = _calculate_list_score(
        count=len(education),
        max_count=MAX_EDUCATION_ENTRIES,
        weight=EDUCATION_SCORE_WEIGHT,
    )
    experience_score = _calculate_list_score(
        count=len(experience),
        max_count=MAX_EXPERIENCE_ENTRIES,
        weight=EXPERIENCE_SCORE_WEIGHT,
    )
    project_score = _calculate_list_score(
        count=len(projects),
        max_count=MAX_PROJECTS_ENTRIES,
        weight=PROJECTS_SCORE_WEIGHT,
    )
    extras_score = _calculate_list_score(
        count=len(certifications) + len(languages),
        max_count=MAX_EXTRAS_ENTRIES,
        weight=EXTRAS_SCORE_WEIGHT,
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
        "Resume score breakdown: contact=%s skills=%s education=%s experience=%s projects=%s extras=%s total=%s",
        contact_score,
        skills_score,
        education_score,
        experience_score,
        project_score,
        extras_score,
        normalized_score,
    )
    return normalized_score


def _extract_string(value: Any) -> str:
    """Convert a value to a stripped string if possible."""
    if isinstance(value, str):
        return value.strip()
    return ""


def _extract_list(value: Any) -> list[str]:
    """Convert a value to a list of strings if possible."""
    if isinstance(value, list):
        return [str(item).strip() for item in value if isinstance(item, str) and item.strip()]
    return []


def _calculate_contact_score(name: str, email: str, phone: str) -> float:
    """Score contact section completeness."""
    present_fields = sum(bool(field) for field in (name, email, phone))
    return (present_fields / 3) * CONTACT_SCORE_WEIGHT


def _calculate_list_score(count: int, max_count: int, weight: int) -> float:
    """Score a list-based resume section using diminishing returns."""
    if count <= 0:
        return 0.0

    normalized = min(count, max_count) / max_count
    return normalized * weight
