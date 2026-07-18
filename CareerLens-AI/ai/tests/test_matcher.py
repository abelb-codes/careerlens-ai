"""Unit tests for the resume-job matching engine."""

from __future__ import annotations

import unittest

from ai.matcher.matcher import match_resume_to_job


class TestMatcher(unittest.TestCase):
    """Test cases for resume-job semantic matching."""

    def test_match_resume_to_job_returns_valid_result(self) -> None:
        resume_profile = {
            "name": "Jane Doe",
            "skills": ["Python", "Django", "AWS"],
            "education": ["BSc Computer Science"],
            "experience": ["Built REST APIs using Django"],
            "projects": ["CRM application with Django and AWS"],
            "certifications": ["AWS Certified Cloud Practitioner"],
            "languages": ["English"],
        }
        job_profile = {
            "job_title": "Senior Backend Engineer",
            "required_skills": ["Python", "Django", "REST API", "AWS"],
            "experience_required": ["3+ years of experience"],
            "education_required": ["bachelor"],
            "keywords": ["backend", "api", "cloud"],
        }

        result = match_resume_to_job(resume_profile, job_profile)

        self.assertIsInstance(result, dict)
        self.assertIn("match_score", result)
        self.assertIn("semantic_similarity", result)
        self.assertGreaterEqual(result["match_score"], 0)
        self.assertLessEqual(result["match_score"], 100)
        self.assertEqual(result["matched_skills"], ["python", "django", "aws"])
        self.assertEqual(result["missing_skills"], ["rest api"])
        self.assertIsInstance(result["matched_keywords"], list)
        self.assertIsInstance(result["missing_keywords"], list)

    def test_match_invalid_input_returns_empty_result(self) -> None:
        result = match_resume_to_job(None, None)  # type: ignore[arg-type]

        self.assertEqual(result, {
            "match_score": 0,
            "semantic_similarity": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "matched_keywords": [],
            "missing_keywords": [],
        })


if __name__ == "__main__":
    unittest.main()
