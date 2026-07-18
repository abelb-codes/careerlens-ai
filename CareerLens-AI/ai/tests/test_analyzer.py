"""
Unit tests for resume quality analysis orchestration.
"""

from __future__ import annotations

import unittest

from ai.analyzer.analyzer import analyze_resume


class TestAnalyzerOrchestrator(unittest.TestCase):
    """Test cases for resume analyzer output."""

    def test_analyze_resume_returns_valid_contract(self) -> None:
        """Analyze resume data and return a complete analyzer contract."""
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

        result = analyze_resume(extracted)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["resume_score"], 51)
        self.assertEqual(result["ats_score"], 100)
        self.assertIn("Complete contact information", result["strengths"])
        self.assertEqual(result["weaknesses"], [])
        self.assertEqual(result["suggestions"], [])

    def test_analyze_resume_handles_invalid_input(self) -> None:
        """Non-dict input returns an empty analysis contract."""
        result = analyze_resume(None)  # type: ignore[arg-type]

        self.assertEqual(result, {
            "resume_score": 0,
            "ats_score": 0,
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
        })


if __name__ == "__main__":
    unittest.main()
