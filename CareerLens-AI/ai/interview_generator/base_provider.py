"""Base provider interface for interview question generation.

This module defines the abstract contract for any interview question provider.
It enables the CareerLens AI interview generator to switch between template
logic and future AI-powered providers without changing the public API.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class InterviewProvider(ABC):
    """Abstract provider interface for generating interview questions."""

    @abstractmethod
    def generate_questions(
        self,
        resume_profile: dict[str, Any] | None,
        job_profile: dict[str, Any] | None,
        matching_result: dict[str, Any] | None,
    ) -> dict[str, list[str]]:
        """Generate interview questions for a candidate.

        Parameters
        ----------
        resume_profile:
            Parsed resume information for the candidate.
        job_profile:
            Parsed job description information.
        matching_result:
            Results returned by the matching engine.

        Returns
        -------
        dict[str, list[str]]
            A dictionary containing exactly five questions under the key
            "questions".
        """
        raise NotImplementedError("InterviewProvider subclasses must implement generate_questions")
