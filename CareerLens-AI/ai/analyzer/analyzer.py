"""
AI resume quality analysis orchestrator.

This module produces a resume quality report from normalized extractor
output. It combines resume scoring, strengths/weaknesses detection, and
improvement suggestions.
"""

from __future__ import annotations

import logging
from typing import Any, TypedDict

from ai.analyzer.ats_score import calculate_ats_score
from ai.analyzer.resume_score import calculate_resume_score
from ai.analyzer.suggestions import generate_resume_suggestions

logger = logging.getLogger(__name__)


class ResumeAnalysisResult(TypedDict):
    """Structured result returned by resume analysis."""

    resume_score: int
    ats_score: int
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]


def analyze_resume(extracted_resume: dict[str, Any]) -> ResumeAnalysisResult:
    """
    Analyze extracted resume data and return a quality report.

    Parameters
    ----------
    extracted_resume:
        A dictionary produced by the extractor contract.

    Returns
    -------
    ResumeAnalysisResult
        A dictionary containing resume quality analysis results.
    """
    if not isinstance(extracted_resume, dict):
        logger.warning("Resume analysis received non-dict input.")
        return _empty_analysis_result()

    resume_score = calculate_resume_score(extracted_resume)
    ats_score = calculate_ats_score(extracted_resume)
    suggestions = generate_resume_suggestions(extracted_resume)
    strengths = _derive_strengths(extracted_resume)
    weaknesses = _derive_weaknesses(extracted_resume)

    return {
        "resume_score": resume_score,
        "ats_score": ats_score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
    }


def _empty_analysis_result() -> ResumeAnalysisResult:
    """Return a default analysis result preserving the analyzer contract."""
    return {
        "resume_score": 0,
        "ats_score": 0,
        "strengths": [],
        "weaknesses": [],
        "suggestions": [],
    }


def _derive_strengths(extracted_resume: dict[str, Any]) -> list[str]:
    """Infer resume strengths from extracted resume sections."""
    strengths: list[str] = []
    skills = _extract_list(extracted_resume.get("skills"))
    education = _extract_list(extracted_resume.get("education"))
    experience = _extract_list(extracted_resume.get("experience"))
    projects = _extract_list(extracted_resume.get("projects"))
    certifications = _extract_list(extracted_resume.get("certifications"))
    languages = _extract_list(extracted_resume.get("languages"))

    if all(extracted_resume.get(key) for key in ("name", "email", "phone")):
        strengths.append("Complete contact information")

    if len(skills) >= 3:
        strengths.append("Strong technical skill set")
    elif skills:
        strengths.append("Skills are identified")

    if education:
        strengths.append("Education history is present")

    if experience:
        strengths.append("Work experience is documented")

    if projects:
        strengths.append("Project work is showcased")

    if certifications or languages:
        strengths.append("Additional qualifications are included")

    return strengths


def _derive_weaknesses(extracted_resume: dict[str, Any]) -> list[str]:
    """Infer resume weaknesses from extracted resume sections."""
    weaknesses: list[str] = []
    skills = _extract_list(extracted_resume.get("skills"))
    education = _extract_list(extracted_resume.get("education"))
    experience = _extract_list(extracted_resume.get("experience"))
    projects = _extract_list(extracted_resume.get("projects"))
    certifications = _extract_list(extracted_resume.get("certifications"))
    languages = _extract_list(extracted_resume.get("languages"))

    if not extracted_resume.get("name"):
        weaknesses.append("Missing candidate name")
    if not extracted_resume.get("email"):
        weaknesses.append("Missing email address")
    if not extracted_resume.get("phone"):
        weaknesses.append("Missing phone number")

    if len(skills) < 3:
        weaknesses.append("Add more relevant skills to improve resume impact")

    if not education:
        weaknesses.append("Include education history to provide background context")

    if not experience:
        weaknesses.append("Add work experience entries to demonstrate professional history")

    if not projects:
        weaknesses.append("Include at least one project to showcase practical experience")

    if not certifications and not languages:
        weaknesses.append("List certifications or languages to strengthen your profile")

    return weaknesses


def _extract_list(value: Any) -> list[str]:
    """Convert a value to a list of stripped strings if possible."""
    if isinstance(value, list):
        return [str(item).strip() for item in value if isinstance(item, str) and item.strip()]
    return []
