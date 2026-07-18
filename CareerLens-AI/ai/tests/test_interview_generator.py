"""Unit tests for the CareerLens AI interview question generator."""

from __future__ import annotations

import unittest

from ai.interview_generator.interview_generator import generate_interview_questions


class TestInterviewGenerator(unittest.TestCase):
    """Tests for interview question generation and edge case handling."""

    def test_generate_interview_questions_returns_five_questions(self) -> None:
        resume_profile = {
            "name": "Jane Doe",
            "skills": ["Python", "Django", "AWS"],
            "experience": ["Built REST APIs"],
            "projects": ["Cloud migration project"],
            "education": ["BSc Computer Science"],
            "certifications": ["AWS Certified"],
            "languages": ["English"],
        }
        job_profile = {
            "job_title": "Backend Engineer",
            "required_skills": ["Python", "Django", "AWS"],
            "experience_required": ["3+ years"],
            "education_required": ["Bachelor's degree"],
            "keywords": ["cloud", "api", "backend"],
        }
        matching_result = {
            "match_score": 92,
            "matched_skills": ["Python", "Django"],
            "missing_skills": ["AWS"],
            "matched_keywords": ["cloud", "api"],
            "missing_keywords": ["backend"],
        }

        result = generate_interview_questions(resume_profile, job_profile, matching_result)

        self.assertIsInstance(result, dict)
        self.assertIn("questions", result)
        self.assertIsInstance(result["questions"], list)
        self.assertEqual(len(result["questions"]), 5)
        for question in result["questions"]:
            self.assertIsInstance(question, str)
            self.assertTrue(question.strip())

    def test_generate_interview_questions_handles_missing_resume_fields(self) -> None:
        resume_profile = {
            "name": "Alex",
            "skills": [],
            "experience": [],
            "projects": [],
        }
        job_profile = {
            "job_title": "Data Analyst",
            "required_skills": ["SQL", "Excel"],
            "keywords": ["data", "analysis"],
        }
        matching_result = {
            "match_score": 40,
            "matched_skills": [],
            "missing_skills": ["SQL"],
            "matched_keywords": [],
            "missing_keywords": ["data"],
        }

        result = generate_interview_questions(resume_profile, job_profile, matching_result)

        self.assertEqual(len(result["questions"]), 5)
        self.assertNotIn("", result["questions"])

    def test_generate_interview_questions_handles_missing_job_fields(self) -> None:
        resume_profile = {
            "name": "Sam",
            "skills": ["Java", "Spring"],
            "experience": ["Built microservices"],
            "projects": ["Inventory management system"],
        }
        job_profile = {}
        matching_result = {
            "match_score": 70,
            "matched_skills": ["Java"],
            "missing_skills": ["Docker"],
            "matched_keywords": [],
            "missing_keywords": [],
        }

        result = generate_interview_questions(resume_profile, job_profile, matching_result)

        self.assertEqual(len(result["questions"]), 5)
        for question in result["questions"]:
            self.assertTrue(isinstance(question, str) and question.strip())

    def test_generate_interview_questions_handles_empty_inputs(self) -> None:
        result = generate_interview_questions({}, {}, {})

        self.assertEqual(len(result["questions"]), 5)
        self.assertEqual(len(set(result["questions"])), 5)

    def test_generate_interview_questions_handles_invalid_inputs(self) -> None:
        result = generate_interview_questions(None, None, None)

        self.assertEqual(len(result["questions"]), 5)
        for question in result["questions"]:
            self.assertTrue(isinstance(question, str) and question.strip())


if __name__ == "__main__":
    unittest.main()
