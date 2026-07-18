# ai/tests/test_parser.py
"""
Unit tests for the Resume Parser subpackage.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from ai.parser.pdf_parser import parse_pdf
from ai.parser.docx_parser import parse_docx
from ai.parser.parser import parse_resume


class TestPDFParser(unittest.TestCase):
    """Test cases for PDF file parsing."""

    def test_parse_pdf_success(self):
        """Test successful parsing of a digital PDF file."""
        mock_doc = MagicMock()
        mock_doc.page_count = 2

        mock_page_1 = MagicMock()
        mock_page_1.get_text.return_value = "Page 1 Resume Text"

        mock_page_2 = MagicMock()
        mock_page_2.get_text.return_value = "Page 2 Resume Text"

        mock_doc.__iter__.return_value = [mock_page_1, mock_page_2]

        fake_fitz = MagicMock()
        fake_fitz.open.return_value.__enter__.return_value = mock_doc

        with patch("ai.parser.pdf_parser.Path.exists", return_value=True), \
             patch("ai.parser.pdf_parser.Path.is_file", return_value=True), \
             patch("ai.parser.pdf_parser.importlib.import_module", return_value=fake_fitz):
            result = parse_pdf("dummy_resume.pdf")

        self.assertTrue(result["success"])
        self.assertEqual(result["file_name"], "dummy_resume.pdf")
        self.assertEqual(result["file_type"], "pdf")
        self.assertEqual(result["pages"], 2)
        self.assertEqual(result["text"], "Page 1 Resume Text\nPage 2 Resume Text")
        self.assertIsNone(result["error"])

    def test_parse_pdf_exception(self):
        """Test parser handles corrupted/invalid PDFs gracefully."""
        fake_fitz = MagicMock()
        fake_fitz.open.side_effect = Exception("Corrupt PDF file structure")

        with patch("ai.parser.pdf_parser.Path.exists", return_value=True), \
             patch("ai.parser.pdf_parser.Path.is_file", return_value=True), \
             patch("ai.parser.pdf_parser.importlib.import_module", return_value=fake_fitz):
            result = parse_pdf("corrupt_resume.pdf")

        self.assertFalse(result["success"])
        self.assertEqual(result["file_name"], "corrupt_resume.pdf")
        self.assertEqual(result["pages"], 0)
        self.assertEqual(result["text"], "")
        self.assertIn("Corrupt PDF file structure", result["error"])


class TestDOCXParser(unittest.TestCase):
    """Test cases for DOCX Word document parsing."""

    def test_parse_docx_success(self):
        """Test successful parsing of paragraphs and tables."""
        mock_doc = MagicMock()

        # Mock standard paragraphs
        mock_p1 = MagicMock()
        mock_p1.text = " John Doe "
        mock_p2 = MagicMock()
        mock_p2.text = " Software Engineer "
        mock_doc.paragraphs = [mock_p1, mock_p2]

        # Mock tables with merged cells to test deduplication
        mock_cell_1 = MagicMock()
        mock_cell_1.text = "Python"
        mock_cell_2 = MagicMock()
        mock_cell_2.text = "Python"  # Merged cell duplicate
        mock_cell_3 = MagicMock()
        mock_cell_3.text = "Django"

        mock_row = MagicMock()
        mock_row.cells = [mock_cell_1, mock_cell_2, mock_cell_3]

        mock_table = MagicMock()
        mock_table.rows = [mock_row]
        mock_doc.tables = [mock_table]

        fake_docx = MagicMock()
        fake_docx.Document.return_value = mock_doc

        with patch("ai.parser.docx_parser.Path.exists", return_value=True), \
             patch("ai.parser.docx_parser.Path.is_file", return_value=True), \
             patch("ai.parser.docx_parser.importlib.import_module", return_value=fake_docx):
            result = parse_docx("resume.docx")

        self.assertTrue(result["success"])
        self.assertEqual(result["file_name"], "resume.docx")
        self.assertEqual(result["file_type"], "docx")
        self.assertEqual(result["pages"], 0)  # Always 0 for DOCX
        self.assertEqual(result["text"], "John Doe\nSoftware Engineer\nPython | Django")
        self.assertIsNone(result["error"])

    def test_parse_docx_exception(self):
        """Test parser handles docx open errors gracefully."""
        fake_docx = MagicMock()
        fake_docx.Document.side_effect = Exception("Invalid zip file format")

        with patch("ai.parser.docx_parser.Path.exists", return_value=True), \
             patch("ai.parser.docx_parser.Path.is_file", return_value=True), \
             patch("ai.parser.docx_parser.importlib.import_module", return_value=fake_docx):
            result = parse_docx("bad.docx")

        self.assertFalse(result["success"])
        self.assertEqual(result["file_name"], "bad.docx")
        self.assertEqual(result["text"], "")
        self.assertIn("Invalid zip file format", result["error"])


class TestParserOrchestrator(unittest.TestCase):
    """Test cases for the unified parser.py entry point."""

    @patch("ai.parser.parser.parse_pdf")
    def test_route_pdf(self, mock_parse_pdf):
        """Test that .pdf extension calls parse_pdf."""
        mock_parse_pdf.return_value = {"success": True}

        with patch("ai.parser.parser.Path.exists", return_value=True), \
             patch("ai.parser.parser.Path.is_file", return_value=True):
            parse_resume("test.pdf")

        mock_parse_pdf.assert_called_once()

    @patch("ai.parser.parser.parse_docx")
    def test_route_docx(self, mock_parse_docx):
        """Test that .docx and .doc extensions call parse_docx."""
        mock_parse_docx.return_value = {"success": True}

        with patch("ai.parser.parser.Path.exists", return_value=True), \
             patch("ai.parser.parser.Path.is_file", return_value=True):
            parse_resume("test.docx")
            parse_resume("test.doc")

        self.assertEqual(mock_parse_docx.call_count, 2)

    def test_unsupported_file_extension(self):
        """Test parser rejects unsupported formats (e.g. .txt)."""
        with patch("ai.parser.parser.Path.exists", return_value=True), \
             patch("ai.parser.parser.Path.is_file", return_value=True):
            result = parse_resume("test.txt")

        self.assertFalse(result["success"])
        self.assertEqual(result["file_type"], "txt")
        self.assertIn("Unsupported file extension", result["error"])

    def test_file_not_found(self):
        """Test file not found scenario returns contract with failure."""
        result = parse_resume("non_existent_file.pdf")
        self.assertFalse(result["success"])
        self.assertIn("File not found", result["error"])

    def test_path_is_directory(self):
        """Test passing a directory fails gracefully."""
        with patch("ai.parser.parser.Path.exists", return_value=True), \
             patch("ai.parser.parser.Path.is_file", return_value=False):
            result = parse_resume("some_dir")
            
        self.assertFalse(result["success"])
        self.assertIn("Path is not a file", result["error"])


if __name__ == "__main__":
    unittest.main()
