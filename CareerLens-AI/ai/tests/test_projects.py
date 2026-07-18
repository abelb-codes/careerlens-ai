# ai/tests/test_projects.py
"""
Unit tests for project extraction.
"""

from __future__ import annotations

import unittest

from ai.extractor.projects import extract_projects


class TestProjectExtraction(unittest.TestCase):
    """Test cases for resume project extraction."""

    def test_extracts_projects_from_section(self) -> None:
        """Extract project lines from a dedicated projects section."""
        text = """
        Skills
        Python, Django
        Projects
        CareerLens AI Platform
        Built a resume intelligence system using Python and Django
        Education
        BSc Computer Science
        """

        result = extract_projects(text)

        self.assertEqual(
            result,
            [
                "CareerLens AI Platform | "
                "Built a resume intelligence system using Python and Django"
            ],
        )

    def test_falls_back_to_project_signals_without_section_header(self) -> None:
        """Find projects even when no projects section header is present."""
        text = """
        Inventory Dashboard
        Developed a dashboard using React and PostgreSQL
        """

        result = extract_projects(text)

        self.assertEqual(
            result,
            ["Inventory Dashboard | Developed a dashboard using React and PostgreSQL"],
        )

    def test_deduplicates_repeated_projects(self) -> None:
        """Avoid returning duplicate project entries."""
        text = """
        Projects
        Portfolio Website
        Portfolio Website
        """

        result = extract_projects(text)

        self.assertEqual(result, ["Portfolio Website"])

    def test_returns_empty_list_for_non_string_input(self) -> None:
        """Keep the extractor stable when invalid input is passed."""
        result = extract_projects(None)  # type: ignore[arg-type]

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
