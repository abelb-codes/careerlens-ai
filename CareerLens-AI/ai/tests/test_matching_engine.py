"""Unit tests for the matcher matching engine."""

from __future__ import annotations

import unittest

from ai.matcher.matching_engine import match_resume_to_job


class TestMatchingEngine(unittest.TestCase):
    """Tests for resume-job matching orchestration."""

    def test_match_resume_to_job_returns_expected_structure(self) -> None:
        resume_profile = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "+1234567890",
            "skills": ["Python", "Django", "AWS"],
            "education": ["BSc Computer Science"],
            "experience": ["Built REST APIs using Django"],
            "projects": ["Backend application with AWS deployment"],
            "certifications": ["AWS Certified"],
            "languages": ["English"],
        }
        job_profile = {
            "job_title": "Senior Backend Engineer",
            "required_skills": ["Python", "Django", "AWS", "REST API"],
            "experience_required": ["REST API"],
            "education_required": ["bachelor"],
            "keywords": ["backend", "cloud", "api"],
        }

        result = match_resume_to_job(resume_profile, job_profile)

        self.assertIsInstance(result, dict)
        self.assertIn("match_score", result)
        self.assertIn("semantic_similarity", result)
        self.assertEqual(result["matched_skills"], ["python", "django", "aws"])
        self.assertEqual(result["missing_skills"], ["rest api"])
        self.assertIn("backend", result["missing_keywords"] + result["matched_keywords"])

    def test_match_resume_to_job_invalid_input_returns_empty(self) -> None:
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
