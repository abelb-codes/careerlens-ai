# ai/tests/test_education.py
"""
Unit tests for education extraction.
"""

from __future__ import annotations

import unittest

from ai.extractor.education import extract_education


class TestEducationExtraction(unittest.TestCase):
    """Test cases for education section extraction."""

    def test_extracts_education_from_section(self) -> None:
        """Extract education lines from a dedicated education section."""
        text = """
        Skills
        Python, Django
        Education
        BSc Computer Science
        University of Nairobi
        2022
        Experience
        Software Developer at Example Ltd
        """

        result = extract_education(text)

        self.assertEqual(
            result,
            ["BSc Computer Science | University of Nairobi | 2022"],
        )

    def test_falls_back_to_education_signals_without_section_header(self) -> None:
        """Find education entries even when no section header is present."""
        text = """
        Jane Doe
        Diploma in Data Analytics
        Moringa School
        """

        result = extract_education(text)

        self.assertEqual(result, ["Diploma in Data Analytics | Moringa School"])

    def test_deduplicates_repeated_entries(self) -> None:
        """Avoid returning duplicate education entries."""
        text = """
        Education
        MSc Data Science
        MSc Data Science
        """

        result = extract_education(text)

        self.assertEqual(result, ["MSc Data Science"])

    def test_returns_empty_list_for_non_string_input(self) -> None:
        """Keep the extractor stable when invalid input is passed."""
        result = extract_education(None)  # type: ignore[arg-type]

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
