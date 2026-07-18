# ai/tests/test_experience.py
"""
Unit tests for experience extraction.
"""

from __future__ import annotations

import unittest

from ai.extractor.experience import extract_experience


class TestExperienceExtraction(unittest.TestCase):
    """Test cases for work experience extraction."""

    def test_extracts_experience_from_section(self) -> None:
        """Extract work experience lines from a dedicated experience section."""
        text = """
        Skills
        Python, Django
        Experience
        Software Engineer at Example Ltd
        Jan 2021 - Present
        Built REST APIs for internal teams
        Education
        BSc Computer Science
        """

        result = extract_experience(text)

        self.assertEqual(
            result,
            [
                "Software Engineer at Example Ltd | "
                "Jan 2021 - Present | "
                "Built REST APIs for internal teams"
            ],
        )

    def test_falls_back_to_experience_signals_without_section_header(self) -> None:
        """Find experience entries even when no section header is present."""
        text = """
        Data Analyst at Acme Corporation
        2020 - 2022
        Improved reporting workflows
        """

        result = extract_experience(text)

        self.assertEqual(
            result,
            ["Data Analyst at Acme Corporation | 2020 - 2022 | Improved reporting workflows"],
        )

    def test_deduplicates_repeated_entries(self) -> None:
        """Avoid returning duplicate work experience entries."""
        text = """
        Work Experience
        Project Manager at Build Ltd
        Project Manager at Build Ltd
        """

        result = extract_experience(text)

        self.assertEqual(result, ["Project Manager at Build Ltd"])

    def test_returns_empty_list_for_non_string_input(self) -> None:
        """Keep the extractor stable when invalid input is passed."""
        result = extract_experience(None)  # type: ignore[arg-type]

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
