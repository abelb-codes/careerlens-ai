"""
Resume improvement suggestions for CareerLens AI.

This module generates actionable recommendations based on extracted resume data.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def generate_resume_suggestions(extracted_resume: dict[str, Any]) -> list[str]:
    """
    Generate resume improvement suggestions from normalized extracted data.

    Parameters
    ----------
    extracted_resume:
        A dictionary produced by the extractor contract.

    Returns
    -------
    list[str]
        A list of actionable improvement suggestions.
    """
    if not isinstance(extracted_resume, dict):
        logger.warning("Resume suggestion generation received non-dict input.")
        return []

    suggestions: list[str] = []
    name = _extract_string(extracted_resume.get("name"))
    email = _extract_string(extracted_resume.get("email"))
    phone = _extract_string(extracted_resume.get("phone"))
    skills = _extract_list(extracted_resume.get("skills"))
    education = _extract_list(extracted_resume.get("education"))
    experience = _extract_list(extracted_resume.get("experience"))
    projects = _extract_list(extracted_resume.get("projects"))
    certifications = _extract_list(extracted_resume.get("certifications"))
    languages = _extract_list(extracted_resume.get("languages"))

    if not name or not email or not phone:
        missing_details = []
        if not name:
            missing_details.append("name")
        if not email:
            missing_details.append("email")
        if not phone:
            missing_details.append("phone number")
        suggestions.append(
            f"Add your {' and '.join(missing_details)} to make it easy for recruiters to contact you."
        )

    if len(skills) < 3:
        suggestions.append(
            "List at least three relevant skills using canonical names such as Python, Django, or AWS."
        )

    if not education:
        suggestions.append(
            "Include education information such as degree, institution, and graduation year."
        )

    if not experience:
        suggestions.append(
            "Add work experience or internship details with role, company, and dates."
        )

    if not projects:
        suggestions.append(
            "Include a project or two that highlights your technical ability and impact."
        )

    if not certifications and not languages:
        suggestions.append(
            "Add certifications or languages to demonstrate additional qualifications."
        )

    return suggestions


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
