"""Unit tests for the job description parser module."""

from __future__ import annotations

import unittest

from ai.matcher.jd_parser import parse_job_description


class TestJobDescriptionParser(unittest.TestCase):
    """Test cases for parsing raw job descriptions into structured profiles."""

    def test_parse_full_job_description(self) -> None:
        raw_text = (
            "Senior Backend Engineer\n"
            "We are looking for a Senior Backend Engineer with 5+ years of experience building REST APIs.\n"
            "Requirements:\n"
            "- Strong Python and Django skills\n"
            "- Experience with AWS, Docker, and Kubernetes\n"
            "- Bachelor degree in Computer Science or related field\n"
        )

        result = parse_job_description(raw_text)

        self.assertEqual(result["job_title"], "Senior Backend Engineer")
        self.assertIn("python", result["required_skills"])
        self.assertIn("django", result["required_skills"])
        self.assertIn("aws", result["required_skills"])
        self.assertIn("docker", result["required_skills"])
        self.assertIn("kubernetes", result["required_skills"])
        self.assertIn("5+ years of experience", result["experience_required"])
        self.assertIn("bachelor", result["education_required"])
        self.assertTrue(result["keywords"])

    def test_parse_job_description_without_title(self) -> None:
        raw_text = (
            "We are hiring a motivated engineer with 3 years experience in backend engineering.\n"
            "Must have Flask, SQL, and AWS.\n"
            "Preferred: Master degree.\n"
        )

        result = parse_job_description(raw_text)

        self.assertEqual(result["job_title"], "We are hiring a motivated engineer with 3 years experience in backend engineering.")
        self.assertIn("flask", result["required_skills"])
        self.assertIn("sql", result["required_skills"])
        self.assertIn("aws", result["required_skills"])
        self.assertIn("master", result["education_required"])
        self.assertEqual(result["experience_required"], ["3 years experience"])

    def test_parse_empty_text_returns_empty_profile(self) -> None:
        result = parse_job_description("")

        self.assertEqual(result, {
            "job_title": "",
            "required_skills": [],
            "experience_required": [],
            "education_required": [],
            "keywords": [],
        })

    def test_parse_non_string_input_returns_empty_profile(self) -> None:
        result = parse_job_description(None)  # type: ignore[arg-type]

        self.assertEqual(result, {
            "job_title": "",
            "required_skills": [],
            "experience_required": [],
            "education_required": [],
            "keywords": [],
        })


if __name__ == "__main__":
    unittest.main()
