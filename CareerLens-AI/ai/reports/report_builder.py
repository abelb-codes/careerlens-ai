"""Report builder for CareerLens AI.

This module aggregates validated outputs from prior phases into a single
structured report. It preserves upstream values without recalculating them
and provides a clean contract for the Django REST API.
"""

from __future__ import annotations

import datetime
import logging
from typing import Any

REPORT_VERSION = "1.0.0"
logger = logging.getLogger(__name__)


class ReportBuilder:
    """Aggregate and validate CareerLens AI module outputs into a report."""

    def __init__(self, version: str | None = None, logger: logging.Logger | None = None) -> None:
        self.version = version or REPORT_VERSION
        self.logger = logger or logger

    def build_report(
        self,
        resume_profile: dict[str, Any] | None,
        resume_analysis: dict[str, Any] | None,
        job_profile: dict[str, Any] | None,
        matching_result: dict[str, Any] | None,
        ranking_result: dict[str, Any] | None,
        interview_questions: list[str] | None,
    ) -> dict[str, Any]:
        """Build a final structured report from prior AI module outputs."""
        candidate = _safe_dict_section(resume_profile, "resume_profile")
        analysis = _safe_dict_section(resume_analysis, "resume_analysis")
        job = _safe_dict_section(job_profile, "job_profile")
        matching = _safe_dict_section(matching_result, "matching_result")
        ranking = _safe_dict_section(ranking_result, "ranking_result")
        questions = _safe_question_list(interview_questions)

        return {
            "candidate": candidate,
            "analysis": analysis,
            "job": job,
            "matching": matching,
            "ranking": ranking,
            "interview_questions": questions,
            "generated_at": _build_generated_at(),
            "version": self.version,
        }


def generate_report(
    resume_profile: dict[str, Any] | None,
    resume_analysis: dict[str, Any] | None,
    job_profile: dict[str, Any] | None,
    matching_result: dict[str, Any] | None,
    ranking_result: dict[str, Any] | None,
    interview_questions: list[str] | None,
    version: str | None = None,
) -> dict[str, Any]:
    """Generate a structured CareerLens AI report."""
    builder = ReportBuilder(version=version)
    return builder.build_report(
        resume_profile,
        resume_analysis,
        job_profile,
        matching_result,
        ranking_result,
        interview_questions,
    )


def _safe_dict_section(value: Any, section_name: str) -> dict[str, Any]:
    if isinstance(value, dict):
        return value

    logger.warning("ReportBuilder received invalid %s; using empty object.", section_name)
    return {}


def _safe_question_list(value: Any) -> list[str]:
    if isinstance(value, list):
        questions: list[str] = []
        for item in value:
            if isinstance(item, str):
                normalized = item.strip()
                if normalized:
                    questions.append(normalized)
            else:
                logger.warning("ReportBuilder ignored non-string interview question: %r", item)
        return questions

    if value is None:
        return []

    logger.warning("ReportBuilder received invalid interview_questions; using empty list.")
    return []


def _build_generated_at() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
