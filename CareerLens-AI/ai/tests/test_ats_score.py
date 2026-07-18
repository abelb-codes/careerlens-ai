"""Unit tests for ATS compatibility scoring."""

from __future__ import annotations

import unittest

from ai.analyzer.ats_score import calculate_ats_score


class TestATSScore(unittest.TestCase):
    """Test cases for ATS compatibility score calculation."""

    def test_complete_resume_gets_high_ats_score(self) -> None:
        extracted = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "+1 555-123-4567",
            "skills": ["Python", "Django", "AWS"],
            "education": ["BSc Computer Science | University of Nairobi | 2022"],
            "experience": ["Software Engineer at Example Ltd | Jan 2021 - Present | Built REST APIs"],
            "projects": ["Built an internal tool with Django and PostgreSQL"],
            "certifications": ["AWS Certified Cloud Practitioner"],
            "languages": ["English"],
        }

        score = calculate_ats_score(extracted)

        self.assertEqual(score, 100)

    def test_missing_sections_reduce_ats_score(self) -> None:
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

        score = calculate_ats_score(extracted)

        self.assertEqual(score, 5)

    def test_invalid_input_returns_zero(self) -> None:
        score = calculate_ats_score(None)  # type: ignore[arg-type]

        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main()
