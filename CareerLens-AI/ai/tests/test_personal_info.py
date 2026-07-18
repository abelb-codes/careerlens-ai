# ai/tests/test_personal_info.py
"""
Unit tests for personal information extraction.
"""

from __future__ import annotations

import unittest

from ai.extractor.personal_info import extract_personal_info


class TestPersonalInfoExtraction(unittest.TestCase):
    """Test cases for extracting candidate contact details."""

    def test_extracts_name_email_and_phone(self) -> None:
        """Extract the main personal details from typical resume header text."""
        text = """
        Jane A. Doe
        Senior Software Engineer
        jane.doe@example.com
        +1 (555) 123-4567
        """

        result = extract_personal_info(text)

        self.assertEqual(result["name"], "Jane A. Doe")
        self.assertEqual(result["email"], "jane.doe@example.com")
        self.assertEqual(result["phone"], "+1 (555) 123-4567")

    def test_returns_empty_values_when_contact_details_are_missing(self) -> None:
        """Return empty strings when no personal details are present."""
        result = extract_personal_info("")

        self.assertEqual(
            result,
            {
                "name": "",
                "email": "",
                "phone": "",
            },
        )

    def test_skips_links_and_job_titles_when_inferring_name(self) -> None:
        """Avoid treating links or role titles as the candidate name."""
        text = """
        LinkedIn: https://linkedin.com/in/janedoe
        Software Engineer
        Jane Doe
        jane@example.com
        """

        result = extract_personal_info(text)

        self.assertEqual(result["name"], "Jane Doe")
        self.assertEqual(result["email"], "jane@example.com")

    def test_returns_empty_schema_for_non_string_input(self) -> None:
        """Keep the extractor contract stable for invalid input types."""
        result = extract_personal_info(None)  # type: ignore[arg-type]

        self.assertEqual(
            result,
            {
                "name": "",
                "email": "",
                "phone": "",
            },
        )


if __name__ == "__main__":
    unittest.main()
