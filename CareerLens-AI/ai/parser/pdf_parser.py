# ai/parser/pdf_parser.py
"""
PDF parser module for extracting raw text from PDF files.
"""

from __future__ import annotations

import importlib
import logging
from pathlib import Path
from typing import Optional

from ai.parser.types import ParserResult

logger = logging.getLogger(__name__)


def parse_pdf(file_path: str | Path) -> ParserResult:
    """
    Extract text and metadata from a PDF file.

    Parameters
    ----------
    file_path : str | Path
        The path to the PDF file.

    Returns
    -------
    ParserResult
        A dictionary matching the Parser Contract.
    """
    path = Path(file_path).resolve()
    result: ParserResult = {
        "success": False,
        "file_name": path.name,
        "file_type": "pdf",
        "pages": 0,
        "text": "",
        "error": None,
    }

    try:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        fitz = importlib.import_module("fitz")

        # Open the PDF document
        with fitz.open(str(path)) as doc:
            result["pages"] = doc.page_count
            extracted_text_parts = []

            for page in doc:
                text_content = page.get_text()
                if text_content:
                    extracted_text_parts.append(text_content)

            result["text"] = "\n".join(extracted_text_parts).strip()
            result["success"] = True
            
    except Exception as exc:
        logger.exception("Failed to parse PDF file at %s", path)
        result["success"] = False
        result["error"] = str(exc)

    return result
