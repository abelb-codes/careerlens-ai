"""Unit tests for the CareerLens AI report builder."""

from __future__ import annotations

import unittest

from ai.reports.report_builder import ReportBuilder, generate_report


class TestReportBuilder(unittest.TestCase):
    """ReportBuilder tests for structured report aggregation."""

    def test_generate_report_includes_all_sections(self) -> None:
        resume_profile = {"name": "Jane Doe", "skills": ["Python"]}
        resume_analysis = {"ats_score": 85, "strengths": ["Python"]}
        job_profile = {"job_title": "Backend Engineer"}
        matching_result = {"match_score": 90, "matched_skills": ["Python"]}
        ranking_result = {"rank": 1, "score": 98}
        interview_questions = ["Tell me about your Python experience."]

        report = generate_report(
            resume_profile,
            resume_analysis,
            job_profile,
            matching_result,
            ranking_result,
            interview_questions,
            version="9.0.0",
        )

        self.assertEqual(report["candidate"], resume_profile)
        self.assertEqual(report["analysis"], resume_analysis)
        self.assertEqual(report["job"], job_profile)
        self.assertEqual(report["matching"], matching_result)
        self.assertEqual(report["ranking"], ranking_result)
        self.assertEqual(report["interview_questions"], interview_questions)
        self.assertEqual(report["version"], "9.0.0")
        self.assertIn("generated_at", report)
        self.assertIsInstance(report["generated_at"], str)

    def test_build_report_handles_none_inputs(self) -> None:
        builder = ReportBuilder()

        report = builder.build_report(None, None, None, None, None, None)

        self.assertEqual(report["candidate"], {})
        self.assertEqual(report["analysis"], {})
        self.assertEqual(report["job"], {})
        self.assertEqual(report["matching"], {})
        self.assertEqual(report["ranking"], {})
        self.assertEqual(report["interview_questions"], [])
        self.assertEqual(report["version"], "1.0.0")

    def test_build_report_ignores_invalid_question_items(self) -> None:
        builder = ReportBuilder(version="report-test")
        interview_questions = ["  What is your leadership style?  ", 123, None, ""]

        report = builder.build_report({}, {}, {}, {}, {}, interview_questions)

        self.assertEqual(report["interview_questions"], ["What is your leadership style?"])
        self.assertEqual(report["version"], "report-test")

    def test_build_report_uses_empty_sections_for_invalid_dicts(self) -> None:
        builder = ReportBuilder()

        report = builder.build_report([], "invalid", 42, "bad", (), {"question": "bad"})

        self.assertEqual(report["candidate"], {})
        self.assertEqual(report["analysis"], {})
        self.assertEqual(report["job"], {})
        self.assertEqual(report["matching"], {})
        self.assertEqual(report["ranking"], {})
        self.assertEqual(report["interview_questions"], [])


if __name__ == "__main__":
    unittest.main()
