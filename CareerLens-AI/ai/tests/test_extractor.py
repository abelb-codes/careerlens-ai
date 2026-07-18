"""
Unit tests for the resume extraction orchestrator.
"""

from __future__ import annotations

import unittest

from ai.extractor.extractor import extract_resume_data


class TestExtractorOrchestrator(unittest.TestCase):
    """Test cases for extracting normalized resume information."""

    def test_extract_resume_data_returns_full_contract(self) -> None:
        """Return all extractor fields when resume text is valid."""
        text = """
        Jane Doe
        jane.doe@example.com
        +1 555-123-4567
        Skills
        Python, Django
        Education
        BSc Computer Science
        University of Nairobi
        2022
        Experience
        Software Engineer at Example Ltd
        Jan 2021 - Present
        Built REST APIs for internal teams
        Projects
        Built an internal tool with Django and PostgreSQL
        Certifications
        AWS Certified Cloud Practitioner
        Languages
        English, Swahili
        """

        result = extract_resume_data(text)

        self.assertEqual(result["name"], "Jane Doe")
        self.assertEqual(result["email"], "jane.doe@example.com")
        self.assertEqual(result["phone"], "+1 555-123-4567")
        self.assertIn("Python", result["skills"])
        self.assertIn("Django", result["skills"])
        self.assertEqual(result["education"], ["BSc Computer Science | University of Nairobi | 2022"])
        self.assertEqual(
            result["experience"],
            [
                "Software Engineer at Example Ltd | Jan 2021 - Present | Built REST APIs for internal teams"
            ],
        )
        self.assertEqual(result["projects"], ["Built an internal tool with Django and PostgreSQL"])
        self.assertEqual(result["certifications"], ["AWS Certified Cloud Practitioner"])
        self.assertEqual(result["languages"], ["English", "Swahili"])

    def test_extract_resume_data_handles_non_string_input(self) -> None:
        """Return an empty extraction contract when input is invalid."""
        result = extract_resume_data(None)  # type: ignore[arg-type]

        self.assertEqual(
            result,
            {
                "name": "",
                "email": "",
                "phone": "",
                "skills": [],
                "education": [],
                "experience": [],
                "projects": [],
                "certifications": [],
                "languages": [],
            },
        )


if __name__ == "__main__":
    unittest.main()
