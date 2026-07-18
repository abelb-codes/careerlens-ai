"""
Unit tests for resume quality scoring.
"""

from __future__ import annotations

import unittest

from ai.analyzer.resume_score import calculate_resume_score


class TestResumeScore(unittest.TestCase):
    """Test cases for resume scoring heuristics."""

    def test_full_resume_scoring(self) -> None:
        """A complete resume receives a high score."""
        extracted = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "+1 555-123-4567",
            "skills": ["Python", "Django", "PostgreSQL"],
            "education": ["BSc Computer Science | University of Nairobi | 2022"],
            "experience": ["Software Engineer at Example Ltd | Jan 2021 - Present | Built REST APIs"],
            "projects": ["Built an internal tool with Django and PostgreSQL"],
            "certifications": ["AWS Certified Cloud Practitioner"],
            "languages": ["English"],
        }

        score = calculate_resume_score(extracted)

        self.assertEqual(score, 51)

    def test_partial_resume_scoring(self) -> None:
        """Missing sections reduce the score but never go below zero."""
        extracted = {
            "name": "",
            "email": "jane.doe@example.com",
            "phone": "",
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "certifications": [],
            "languages": [],
        }

        score = calculate_resume_score(extracted)

        self.assertEqual(score, 3)  # only email present out of contact fields

    def test_invalid_input_returns_zero(self) -> None:
        """Non-dict input should be handled gracefully."""
        score = calculate_resume_score(None)  # type: ignore[arg-type]

        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main()
