"""Interview generator public API for CareerLens AI.

This module exposes the single entrypoint for generating interview questions.
It delegates generation to a pluggable provider and shields the rest of the
application from provider implementation details.
"""

from __future__ import annotations

import logging
from typing import Any

from ai.interview_generator.base_provider import InterviewProvider
from ai.interview_generator.template_provider import TemplateInterviewProvider

logger = logging.getLogger(__name__)


def generate_interview_questions(
    resume_profile: dict[str, Any] | None,
    job_profile: dict[str, Any] | None,
    matching_result: dict[str, Any] | None,
    provider: InterviewProvider | None = None,
) -> dict[str, list[str]]:
    """Generate interview questions for one candidate.

    Parameters
    ----------
    resume_profile:
        Parsed resume profile dictionary.
    job_profile:
        Parsed job profile dictionary.
    matching_result:
        Matching result dictionary from the matcher engine.
    provider:
        Optional custom interview provider. If omitted, uses the template provider.

    Returns
    -------
    dict[str, list[str]]
        Dictionary containing exactly five questions under the key "questions".
    """
    if provider is None:
        provider = TemplateInterviewProvider()

    if not hasattr(provider, "generate_questions"):
        logger.warning("Invalid interview provider supplied; falling back to template provider.")
        provider = TemplateInterviewProvider()

    try:
        return provider.generate_questions(resume_profile, job_profile, matching_result)
    except Exception as error:  # pragma: no cover
        logger.exception("Interview question generation failed.")
        return {"questions": [
            "Describe your most important technical achievement.",
            "Explain how you adapt to new job requirements.",
            "Describe a project where you solved a difficult problem.",
            "What is one skill you are working to improve, and why?",
            "How do you prepare for the responsibilities of this role?",
        ]}
