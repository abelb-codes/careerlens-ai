"""Integration tests for CareerLens AI pipeline orchestration."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from ai.pipeline.applicant_pipeline import ApplicantPipeline
from ai.pipeline.exceptions import InvalidPipelineInputError, PipelineExecutionError
from ai.pipeline.recruiter_pipeline import RecruiterPipeline


class TestApplicantPipeline(unittest.TestCase):
    def test_process_applicant_valid_flow(self) -> None:
        fake_parser = MagicMock(return_value={"text": "John Doe"})
        fake_extractor = MagicMock(return_value={"name": "John Doe", "skills": ["Python"]})
        fake_analyzer = MagicMock(return_value={"resume_score": 90, "ats_score": 85})
        fake_matcher = MagicMock(return_value={"match_score": 88})
        fake_interview_generator = MagicMock(return_value={"questions": ["Why Python?"]})
        fake_report_builder = MagicMock(return_value={"candidate": {}, "version": "1.0.0"})

        pipeline = ApplicantPipeline(
            parser=fake_parser,
            extractor=fake_extractor,
            analyzer=fake_analyzer,
            matcher=fake_matcher,
            interview_generator=fake_interview_generator,
            report_builder=fake_report_builder,
        )

        result = pipeline.process_applicant("/tmp/resume.pdf", {"job_title": "Dev"})

        self.assertEqual(result["resume_profile"], {"name": "John Doe", "skills": ["Python"]})
        self.assertEqual(result["matching_result"], {"match_score": 88})
        self.assertEqual(result["interview_questions"], ["Why Python?"])
        fake_report_builder.assert_called_once()

    def test_process_applicant_invalid_resume_path(self) -> None:
        pipeline = ApplicantPipeline()

        with self.assertRaises(InvalidPipelineInputError):
            pipeline.process_applicant("", {"job_title": "Dev"})


class TestRecruiterPipeline(unittest.TestCase):
    @patch("ai.pipeline.applicant_pipeline.ApplicantPipeline.process_applicant")
    def test_process_candidates_ranks_and_reports(self, mock_process_applicant: MagicMock) -> None:
        mock_process_applicant.side_effect = [
            {
                "candidate_report": {"candidate": {"name": "Alice"}},
                "resume_profile": {"name": "Alice"},
                "resume_analysis": {"resume_score": 90, "ats_score": 80},
                "matching_result": {"match_score": 85},
                "interview_questions": ["Question 1"],
                "error": "",
            },
            {
                "candidate_report": {"candidate": {"name": "Bob"}},
                "resume_profile": {"name": "Bob"},
                "resume_analysis": {"resume_score": 70, "ats_score": 75},
                "matching_result": {"match_score": 70},
                "interview_questions": ["Question 2"],
                "error": "",
            },
        ]

        pipeline = RecruiterPipeline()
        result = pipeline.process_candidates(
            {"job_title": "Dev"},
            ["/tmp/resume-a.pdf", "/tmp/resume-b.pdf"],
        )

        self.assertEqual(len(result["candidate_reports"]), 2)
        self.assertEqual(len(result["ranked_candidates"]), 2)
        self.assertEqual(result["job_profile"], {"job_title": "Dev"})

    @patch("ai.pipeline.applicant_pipeline.ApplicantPipeline.process_applicant")
    def test_process_candidates_invalid_inputs(self, mock_process_applicant: MagicMock) -> None:
        pipeline = RecruiterPipeline()

        with self.assertRaises(InvalidPipelineInputError):
            pipeline.process_candidates("not-a-dict", ["/tmp/resume.pdf"])

        with self.assertRaises(InvalidPipelineInputError):
            pipeline.process_candidates({"job_title": "Dev"}, "not-a-list")

        with self.assertRaises(InvalidPipelineInputError):
            pipeline.process_candidates({"job_title": "Dev"}, [])


if __name__ == "__main__":
    unittest.main()
