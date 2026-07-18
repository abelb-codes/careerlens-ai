# ai/tests/test_skills.py
"""
Unit tests for skills extraction.
"""

from __future__ import annotations

import unittest

from ai.extractor.skills import extract_skills


class TestSkillsExtraction(unittest.TestCase):
    """Test cases for dictionary-based skill extraction."""

    def test_extracts_canonical_skill_names(self) -> None:
        """Extract matching skills using their canonical output names."""
        text = "Built APIs with python, Django, PostgreSQL, Docker, and AWS."

        result = extract_skills(text)

        self.assertEqual(result, ["AWS", "Django", "Docker", "PostgreSQL", "Python"])

    def test_deduplicates_aliases(self) -> None:
        """Map aliases to one canonical skill name."""
        text = "Experience with postgres, PostgreSQL, nodejs, and Node.js."

        result = extract_skills(text)

        self.assertEqual(result, ["Node.js", "PostgreSQL"])

    def test_avoids_common_short_skill_false_positives(self) -> None:
        """Avoid matching short skill names inside ordinary words."""
        text = "I go to meetings and manage risk, but use Golang and R for analytics."

        result = extract_skills(text)

        self.assertIn("Go", result)
        self.assertIn("R", result)
        self.assertNotIn("Git", result)

    def test_returns_empty_list_for_non_string_input(self) -> None:
        """Keep the extractor stable when invalid input is passed."""
        result = extract_skills(None)  # type: ignore[arg-type]

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
